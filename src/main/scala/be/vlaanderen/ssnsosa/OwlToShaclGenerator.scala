package be.vlaanderen.ssnsosa

import org.apache.jena.rdf.model._
import org.apache.jena.vocabulary.{OWL, RDF, RDFS}

import scala.jdk.CollectionConverters._

private sealed trait ValueKind
private case class SingleValue(uri: String, isDatatype: Boolean) extends ValueKind
private case class OrValue(members: List[(String, Boolean)]) extends ValueKind

object OwlToShaclGenerator {

  val SH = "http://www.w3.org/ns/shacl#"

  // ---------------------------
  // Helpers
  // ---------------------------

  private def shaclProp(local: String, m: Model): Property =
    m.createProperty(SH + local)

  private def isDatatype(res: Resource): Boolean =
    res.isURIResource &&
      res.getURI.startsWith("http://www.w3.org/2001/XMLSchema#")

  private def createPath(prop: Resource, shacl: Model): RDFNode = {
    if (prop.isAnon) {
      Option(prop.getPropertyResourceValue(OWL.inverseOf)) match {
        case Some(inv) if inv.isURIResource =>
          val b = shacl.createResource()
          b.addProperty(shaclProp("inversePath", shacl), inv)
          return b
        case _ =>
      }
    }
    shacl.createResource(prop.getURI)
  }

  // Een restrictie met expliciet owl:minCardinality 0 op een property van een klasse geldt als
  // aanwijzing "in SHACL niet verplicht": een owl:someValuesFrom op dezelfde klasse en property
  // krijgt dan geen impliciete sh:minCount 1. Zo kan een profiel (bv. waterkwaliteit.ttl) de
  // existentiële restricties van een geïmporteerde ontologie (bv. csor.ttl) behouden zonder dat
  // data die naar die concepten verwijst, de registergegevens moet dupliceren.
  private def pathsMetMinCardinaliteitNul(restrictions: List[Resource]): Set[String] =
    restrictions.flatMap { r =>
      val onProp = r.getPropertyResourceValue(OWL.onProperty)
      val nul = Option(r.getProperty(OWL.minCardinality)).map(_.getObject).exists {
        case l: Literal => l.getInt == 0
        case _ => false
      }
      if (onProp != null && onProp.isURIResource && nul) Some(onProp.getURI) else None
    }.toSet

  private def valueKind(restriction: Resource): Option[ValueKind] = {
    val some = Option(restriction.getPropertyResourceValue(OWL.someValuesFrom))
    val all  = Option(restriction.getPropertyResourceValue(OWL.allValuesFrom))

    some.orElse(all).collect {
      case v if v.hasProperty(OWL.unionOf) =>
        val members =
          v.getPropertyResourceValue(OWL.unionOf)
            .as(classOf[RDFList])
            .iterator().asScala
            .collect { case r: Resource if r.isURIResource => (r.getURI, isDatatype(r)) }
            .toList
            .sortBy(_._1)
        OrValue(members)

      case v if v.isURIResource =>
        SingleValue(v.getURI, isDatatype(v))
    }
  }

  private def intValue(restriction: Resource, p: Property): Option[Int] =
    Option(restriction.getProperty(p))
      .map(_.getObject)
      .collect { case l: Literal => l.getInt }

  private def minCount(restriction: Resource, versoepeld: Set[String]): Option[Int] = {
    val onProp = restriction.getPropertyResourceValue(OWL.onProperty)
    intValue(restriction, OWL.cardinality)
      .orElse(intValue(restriction, OWL.minCardinality))
      .orElse(
        if (restriction.hasProperty(OWL.someValuesFrom) &&
          !(onProp.isURIResource && versoepeld.contains(onProp.getURI)))
          Some(1)
        else None
      )
      .filter(_ > 0)   // sh:minCount 0 is nietszeggend
  }

  private def maxCount(restriction: Resource): Option[Int] =
    intValue(restriction, OWL.cardinality)
      .orElse(intValue(restriction, OWL.maxCardinality))

  // Sleutel van het pad: de property-IRI, of "^IRI" voor een owl:inverseOf-property.
  private def padSleutel(onProp: Resource): Option[String] =
    if (onProp.isURIResource) Some(onProp.getURI)
    else Option(onProp.getPropertyResourceValue(OWL.inverseOf))
      .filter(_.isURIResource)
      .map("^" + _.getURI)

  private def addClassOrDatatype(ps: Resource, uri: String, isDt: Boolean, shacl: Model): Unit =
    ps.addProperty(shaclProp(if (isDt) "datatype" else "class", shacl), shacl.createResource(uri))

  // ---------------------------
  // owl:unionOf → sh:or
  // ---------------------------

  private def createOrList(members: List[(String, Boolean)], shacl: Model): RDFNode = {
    val shapes = members.map { case (uri, isDt) =>
      val ps = shacl.createResource()
      addClassOrDatatype(ps, uri, isDt, shacl)
      ps
    }
    shacl.createList(shapes.iterator.asJava)
  }

  // ---------------------------
  // PropertyShape generation
  // ---------------------------

  // Eén property shape per pad: alle restricties van de klasse op dezelfde property worden
  // samengevoegd. Meerdere sh:class/sh:or in één shape moeten alle gelden, net als de
  // intersectie van de OWL-restricties; sh:minCount is het grootste minimum, sh:maxCount het
  // kleinste maximum.
  private def generatePropertyShape(
                                     onProp: Resource,
                                     restrictions: List[Resource],
                                     shacl: Model,
                                     nodeShape: Resource,
                                     versoepeld: Set[String]
                                   ): Unit = {

    val ps = shacl.createResource()
    ps.addProperty(shaclProp("path", shacl), createPath(onProp, shacl))

    restrictions.flatMap(valueKind).distinct.foreach {
      case SingleValue(uri, isDt) => addClassOrDatatype(ps, uri, isDt, shacl)
      case OrValue(members)       => ps.addProperty(shaclProp("or", shacl), createOrList(members, shacl))
    }

    val mins = restrictions.flatMap(minCount(_, versoepeld))
    val maxs = restrictions.flatMap(maxCount)
    if (mins.nonEmpty) ps.addLiteral(shaclProp("minCount", shacl), mins.max)
    if (maxs.nonEmpty) ps.addLiteral(shaclProp("maxCount", shacl), maxs.min)

    nodeShape.addProperty(shaclProp("property", shacl), ps)
  }

  // ---------------------------
  // NodeShape generation
  // ---------------------------

  private def generateNodeShape(cls: Resource, ontology: Model, shacl: Model): Unit = {

    val ns = shacl.createResource(cls.getURI + "Shape")
    ns.addProperty(RDF.`type`, shacl.createResource(SH + "NodeShape"))
    ns.addProperty(shaclProp("targetClass", shacl), cls)

    val restrictions = ontology
      .listStatements(cls, RDFS.subClassOf, null)
      .asScala
      .map(_.getObject)
      .collect {
        case r: Resource if r.hasProperty(RDF.`type`, OWL.Restriction) &&
          r.getPropertyResourceValue(OWL.onProperty) != null => r
      }
      .toList
    val versoepeld = pathsMetMinCardinaliteitNul(restrictions)

    restrictions
      .flatMap { r =>
        val onProp = r.getPropertyResourceValue(OWL.onProperty)
        padSleutel(onProp).map(k => (k, onProp, r))
      }
      .groupBy(_._1)
      .toList
      .sortBy(_._1)
      .foreach { case (_, groep) =>
        generatePropertyShape(groep.head._2, groep.map(_._3), shacl, ns, versoepeld)
      }
  }

  // ---------------------------
  // Public API
  // ---------------------------

  def generate(ontology: Model): Model = {
    val shacl = ModelFactory.createDefaultModel()

    shacl.setNsPrefix("sh", SH)
    shacl.setNsPrefix("owl", OWL.NS)
    shacl.setNsPrefix("rdfs", RDFS.getURI)

    ontology
      .listResourcesWithProperty(RDF.`type`, OWL.Class)
      .asScala
      .filter(_.isURIResource)
      .foreach(generateNodeShape(_, ontology, shacl))

    shacl
  }
}
