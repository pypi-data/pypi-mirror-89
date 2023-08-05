import os, sys
import site
import unittest
import ctypes as ct

# add the source directory to path so we can import code we are testing
_PYTHON_TESTS_DIR = os.path.dirname(__file__)
_TESTS_DIR = os.path.dirname(_PYTHON_TESTS_DIR)
_PROJECT_ROOT = os.path.dirname(_TESTS_DIR)
_SRC_DIR = os.path.join(_PROJECT_ROOT, "src")

sys.path.append(_SRC_DIR)


from pyomexmeta import PyOmexMetaAPI, eUriType, eXmlType
from test_strings import TestStrings


class TestAPI(unittest.TestCase):
    maxDiff = None
    
    pyom = PyOmexMetaAPI()

    def setUp(self) -> None:
        # loads the function that makes a new RDF
        self.rdf = self.pyom.rdf_new(
            "memory".encode(), "semsim_store".encode(),
            None, None
        )

    def tearDown(self) -> None:
        """calls the RDF delete function after each test"""
        self.pyom.rdf_delete(self.rdf)

    def test_rdf_obj(self):
        self.assertIsInstance(self.rdf, int)

    def test_rdf_size(self):
        rdf = self.pyom.rdf_from_string(
            TestStrings.singular_annotation2.encode(), 'rdfxml'.encode(), "test_rdf_from_string.rdf".encode(),
            "memory".encode(), "libOmexMetaStore".encode(), None, None
        )
        expected = 1
        actual = self.pyom.rdf_size(rdf)
        self.assertEqual(expected, actual)
        self.pyom.rdf_delete(rdf)

    def test_rdf_from_string(self):
        rdf = self.pyom.rdf_from_string(
            TestStrings.singular_annotation2.encode(), 'rdfxml'.encode(), "test_rdf_from_string.rdf".encode(),
            "memory".encode(), "libOmexMetaStore".encode(), None, None
        )
        expected = 1
        actual = self.pyom.rdf_size(rdf)
        self.assertEqual(expected, actual)
        self.pyom.rdf_delete(rdf)

    def test_rdf_add_from_string(self):
        self.pyom.rdf_add_from_string(self.rdf, TestStrings.singular_annotation2.encode(), 'rdfxml'.encode(),
                                          "test_rdf_from_string.rdf".encode())
        expected = 1
        actual = self.pyom.rdf_size(self.rdf)
        self.assertEqual(expected, actual)

    def test_rdf_from_uri(self):
        sbml_url = "https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000064.2?filename=BIOMD0000000064_url.xml"

        rdf = self.pyom.rdf_from_uri(
            sbml_url.encode(), 'rdfxml'.encode(),
            "hashes".encode(), "semsim_hash".encode(), None, None
        )
        expected = 277
        actual = self.pyom.rdf_size(rdf)
        self.assertEqual(expected, actual)
        self.pyom.rdf_delete(rdf)

    def test_rdf_add_from_uri(self):
        sbml_url = "https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000064.2?filename=BIOMD0000000064_url.xml"

        self.pyom.rdf_add_from_uri(self.rdf, sbml_url.encode(), 'rdfxml'.encode())
        expected = 277
        actual = self.pyom.rdf_size(self.rdf)
        self.assertEqual(expected, actual)

    def test_rdf_from_file(self):
        fname = os.path.join(os.getcwd(), "test_rdf_from_file.rdf")
        with open(fname, "w") as f:
            f.write(TestStrings.singular_annotation2)

        rdf = self.pyom.rdf_from_file(
            fname.encode(), 'rdfxml'.encode(),
            "hashes".encode(), "semsim_hash".encode(), None, None)
        expected = 1
        actual = self.pyom.rdf_size(rdf)
        self.assertEqual(expected, actual)
        os.remove(fname)
        self.pyom.rdf_delete(rdf)

    def test_rdf_add_from_file(self):
        fname = os.path.join(os.getcwd(), "test_rdf_from_file.rdf")
        with open(fname, "w") as f:
            f.write(TestStrings.singular_annotation2)

        self.pyom.rdf_add_from_file(self.rdf, fname.encode(), 'rdfxml'.encode())
        expected = 1
        actual = self.pyom.rdf_size(self.rdf)
        self.assertEqual(expected, actual)
        os.remove(fname)

    def test_rdf_to_string(self):
        self.pyom.rdf_add_from_string(self.rdf, TestStrings.singular_annotation2.encode(),
                                          "rdfxml".encode(), "test_rdf_to_string.rdf".encode())
        string_ptr = self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        actual2 = self.pyom.get_and_free_c_str(string_ptr)
        print(actual2)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix bqmodel: <http://biomodels.net/model-qualifiers/> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#modelmeta1>
    bqmodel:isDescribedBy <https://identifiers.org/pubmed/12991237> .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))

    def test_rdf_to_file(self):
        self.pyom.rdf_add_from_string(self.rdf, TestStrings.singular_annotation2.encode(),
                                          "rdfxml".encode(), "test_rdf_to_string.rdf".encode())
        fname = os.path.join(os.path.dirname(__file__), "annotations.rdf")
        self.pyom.rdf_to_file(self.rdf, "rdfxml-abbrev".encode(), fname.encode())
        self.assertTrue(os.path.isfile(fname))
        os.remove(fname)

    def test_rdf_to_editor(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        self.assertIsInstance(editor_ptr, int)
        self.pyom.editor_delete(editor_ptr)

    def test_rdf_query_results_as_str(self):
        self.pyom.rdf_add_from_string(self.rdf, TestStrings.singular_annotation2.encode(),
                                          "rdfxml".encode(), "test_rdf_to_string.rdf".encode())
        query = """
        SELECT ?x ?y ?z 
        WHERE {
            ?x ?y ?z
        }
        """
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_query_results_as_str(self.rdf, query.encode(), "csv".encode())
        )
        expected = """x,y,z
http://omex-library.org/NewOmex.omex/NewModel.xml#modelmeta1,http://biomodels.net/model-qualifiers/isDescribedBy,https://identifiers.org/pubmed/12991237
"""
        self.assertEqual(expected, actual)

    def test_rdf_get_repository(self):
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_get_repository_uri(self.rdf)
        )
        expected = "http://omex-library.org/"
        self.assertEqual(expected, actual)

    def test_rdf_get_archive_uri(self):
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_get_archive_uri(self.rdf)
        )
        expected = "http://omex-library.org/NewOmex.omex/"
        self.assertEqual(expected, actual)

    def test_rdf_get_model_uri(self):
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_get_model_uri(self.rdf)
        )
        expected = "http://omex-library.org/NewOmex.omex/NewModel.xml"
        self.assertEqual(expected, actual)

    def test_rdf_get_local_uri(self):
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_get_local_uri(self.rdf)
        )
        expected = "http://omex-library.org/NewOmex.omex/NewModel.rdf#"
        self.assertEqual(expected, actual)

    def test_rdf_set_repository(self):
        self.pyom.rdf_set_repository_uri(self.rdf, "http://my-awesome-omex.org/".encode())
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_get_repository_uri(self.rdf)
        )
        expected = "http://my-awesome-omex.org/"
        self.assertEqual(expected, actual)

    def test_rdf_set_archive_uri(self):
        self.pyom.rdf_set_archive_uri(self.rdf, "my-awesome-omex.omex".encode())
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_get_archive_uri(self.rdf)
        )
        expected = "http://omex-library.org/my-awesome-omex.omex/"
        self.assertEqual(expected, actual)

    def test_rdf_set_model_uri(self):
        self.pyom.rdf_set_model_uri(self.rdf, "my-awesome-model.sbml".encode())
        actual_model = self.pyom.get_and_free_c_str(
            self.pyom.rdf_get_model_uri(self.rdf)
        )
        actual_local = self.pyom.get_and_free_c_str(
            self.pyom.rdf_get_local_uri(self.rdf)
        )
        expected_model = "http://omex-library.org/NewOmex.omex/my-awesome-model.sbml#"
        expected_local = "http://omex-library.org/NewOmex.omex/my-awesome-model.rdf#"
        self.assertEqual(expected_model, actual_model)
        self.assertEqual(expected_local, actual_local)

    def test_editor_add_namespace(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        self.pyom.editor_add_namespace(editor_ptr, "https://namespace.com".encode(), "ns_".encode())
        singular_annotation = self.pyom.editor_new_singular_annotation(editor_ptr)
        singular_annotation = self.pyom.singular_annotation_about(singular_annotation, "cytosol".encode(), eUriType.MODEL_URI)
        singular_annotation = self.pyom.singular_annotation_set_predicate_from_uri(singular_annotation,
                                                                                       "https://predicate.com/from/uri".encode())
        singular_annotation = self.pyom.singular_annotation_set_resource_uri(singular_annotation,
                                                                                 "http://uri.com/resource".encode())
        self.pyom.editor_add_single_annotation(editor_ptr, singular_annotation)

        expected = r"""<?xml version="1.1" encoding="utf-8"?>
<rdf:RDF xmlns:OMEXlib="http://omex-library.org/"
   xmlns:local="http://omex-library.org/NewOmex.omex/NewModel.rdf#"
   xmlns:myOMEX="http://omex-library.org/NewOmex.omex/"
   xmlns:ns_="https://namespace.com"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="http://uri.com#cytosol">
    <ns1:uri xmlns:ns1="https://predicate.com/from/"
       rdf:resource="http://uri.com/resource"/>
  </rdf:Description>
</rdf:RDF>
"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "rdfxml-abbrev".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.singular_annotation_delete(singular_annotation)

    def test_editor_new_singular_annotation(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        singular_annotation = self.pyom.editor_new_singular_annotation(editor_ptr)
        self.assertIsInstance(singular_annotation, int)
        self.pyom.singular_annotation_delete(singular_annotation)
        self.pyom.editor_delete(editor_ptr)

    def test_editor_new_physical_entity(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        physical_entity = self.pyom.editor_new_physical_entity(editor_ptr)
        self.assertIsInstance(physical_entity, int)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_entity_delete(physical_entity)

    def test_editor_new_physical_process(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        physical_process = self.pyom.editor_new_physical_process(editor_ptr)
        self.assertIsInstance(physical_process, int)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_process_delete(physical_process)

    def test_editor_new_energy_diff(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        energy_diff = self.pyom.editor_new_energy_diff(editor_ptr)
        self.assertIsInstance(energy_diff, int)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.energy_diff_delete(energy_diff)

    def test_editor_get_metaid(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        ptr = self.pyom.editor_get_metaid(editor_ptr, 0)
        actual = self.pyom.get_and_free_c_str(ptr)
        expected = "OmexMetaId0000"
        self.pyom.editor_delete(editor_ptr)

    def test_editor_get_num_metaids(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        actual = self.pyom.editor_get_num_metaids(editor_ptr)
        expected = 13
        self.pyom.editor_delete(editor_ptr)
        self.assertEqual(expected, actual)

    def test_editor_get_xml(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.editor_get_xml(editor_ptr)
        )
        print(actual)
        expected = """<?xml version="1.1" encoding="UTF-8"?>
<sbml xmlns="http://www.sbml.org/sbml/level3/version2/core" level="3" version="2">
      <model id="TestModelNotAnnotated" metaid="model0000">
        <listOfUnitDefinitions>
          <unitDefinition id="molar">
            <listOfUnits>
              <unit kind="mole" exponent="1" scale="1" multiplier="1" metaid="unit0000"/>
              <unit kind="litre" exponent="-1" scale="1" multiplier="1" metaid="unit0001"/>
            </listOfUnits>
          </unitDefinition>
        </listOfUnitDefinitions>
        <listOfCompartments>
          <compartment metaid="cytosol" id="cytosol" size="1" constant="True"/>
        </listOfCompartments>
        <listOfSpecies>
          <species metaid="Meta00001" id="X" compartment="cytosol" initialConcentration="10" substanceUnits="molar" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
          <species id="Y" compartment="cytosol" initialConcentration="20" substanceUnits="molar" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false" metaid="species0000"/>
          <species id="Y" compartment="cytosol" initialConcentration="15" substanceUnits="molar" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false" metaid="species0001"/>
        </listOfSpecies>
        <listOfReactions>
          <reaction id="X2Y" reversible="false" metaid="reaction0000">
            <listOfProducts>
              <speciesReference species="Y" constant="false"/>
            </listOfProducts>
            <kineticLaw metaid="kineticLaw0000">
              <math xmlns="http://www.w3.org/1998/Math/MathML">
                <apply>
                  <times/>
                  <ci> x </ci>
                  <ci> kx2y </ci>
                </apply>
              </math>
              <listOfLocalParameters>
                <localParameter id="kx2y" value="1" metaid="localParameter0000"/>
                <localParameter id="ky2z" value="1" metaid="localParameter0001"/>
              </listOfLocalParameters>
            </kineticLaw>
          </reaction>
          <reaction id="y2z" reversible="false" metaid="reaction0001">
            <listOfProducts>
              <speciesReference species="Z" constant="false"/>
            </listOfProducts>
            <kineticLaw metaid="kineticLaw0001">
              <math xmlns="http://www.w3.org/1998/Math/MathML">
                <apply>
                  <times/>
                  <ci> y </ci>
                  <ci> ky2z </ci>
                </apply>
              </math>
            </kineticLaw>
          </reaction>
        </listOfReactions>
      </model>
    </sbml>
"""
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)

    def test_editor_get_archive_uri(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.editor_get_archive_uri(editor_ptr)
        )
        expected = "http://omex-library.org/NewOmex.omex/"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)

    def test_editor_get_local_uri(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.editor_get_local_uri(editor_ptr)
        )
        expected = "http://omex-library.org/NewOmex.omex/NewModel.rdf#"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)

    def test_editor_get_model_uri(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.editor_get_model_uri(editor_ptr)
        )
        expected = "http://omex-library.org/NewOmex.omex/NewModel.xml"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)

    def test_editor_get_repository_uri(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.editor_get_repository_uri(editor_ptr)
        )
        expected = "http://omex-library.org/"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)

    def test_editor_add_creator(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        self.pyom.editor_add_creator(editor_ptr, "1234-1234-1234-1234".encode())
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        )
        print(actual)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dc: <https://dublincore.org/specifications/dublin-core/dcmi-terms/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    dc:creator <https://orchid.org/1234-1234-1234-1234> .
"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)

    def test_editor_add_curator(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        self.pyom.editor_add_curator(editor_ptr, "1234-1234-1234-1234".encode())
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        )
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dc: <https://dublincore.org/specifications/dublin-core/dcmi-terms/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.rdf#>
    dc:creator <https://orchid.org/1234-1234-1234-1234> .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)

    def test_editor_get_taxon(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        self.pyom.editor_add_taxon(editor_ptr, "9898".encode())
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        )
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix NCBI_Taxon: <https://identifiers.org/taxonomy:> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    bqbiol:hasTaxon <https://identifiers.org/taxonomy:9898> .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)

    def test_editor_add_pubmed(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        self.pyom.editor_add_pubmed(editor_ptr, "1234568".encode())
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        )
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix bqmodel: <http://biomodels.net/model-qualifiers/> .
@prefix pubmed: <https://identifiers.org/pubmed:> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    bqmodel:isDescribedBy <https://identifiers.org/pubmed:1234568> .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)

    def test_editor_add_description(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        self.pyom.editor_add_description(editor_ptr, "An awesome model".encode())
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        )
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dc: <https://dublincore.org/specifications/dublin-core/dcmi-terms/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    dc:description "An awesome model"^^rdf:string .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)

    def test_editor_add_date_created(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        self.pyom.editor_add_date_created(editor_ptr, "14/01/1001".encode())
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        )
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dc: <https://dublincore.org/specifications/dublin-core/dcmi-terms/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    dc:created [
        dc:W3CDTF "14/01/1001"^^rdf:string
    ] .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)

    def test_editor_add_parent_model(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        self.pyom.editor_add_parent_model(editor_ptr, "BIOMDtoomany0s1.xml".encode())
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        )
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix bqmodel: <http://biomodels.net/model-qualifiers/> .
@prefix biomod: <https://identifiers.org/biomodels.db:> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    bqmodel:isDerivedFrom <https://identifiers.org/biomodels.db:BIOMDtoomany0s1.xml> .


"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)

    def test_singular_annotation_about(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        singular_annotation = self.pyom.editor_new_singular_annotation(editor_ptr)
        self.pyom.singular_annotation_about(singular_annotation, "cytosol".encode())
        ptr = self.pyom.singular_annotation_get_about(singular_annotation)
        actual = self.pyom.get_and_free_c_str(ptr)
        expected = "http://omex-library.org/NewOmex.omex/NewModel.xml#cytosol"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.singular_annotation_delete(singular_annotation)

    def test_singular_annotation_predicate(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        singular_annotation = self.pyom.editor_new_singular_annotation(editor_ptr)
        self.pyom.singular_annotation_set_predicate(singular_annotation, "bqbiol".encode(), "is".encode())
        ptr = self.pyom.singular_annotation_get_predicate(singular_annotation)
        actual = self.pyom.get_and_free_c_str(ptr)
        expected = "http://biomodels.net/biology-qualifiers/is"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.singular_annotation_delete(singular_annotation)

    def test_singular_annotation_predicate2(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        singular_annotation = self.pyom.editor_new_singular_annotation(editor_ptr)
        self.pyom.singular_annotation_predicate(singular_annotation, "bqbiol".encode(), "is".encode())
        ptr = self.pyom.singular_annotation_get_predicate(singular_annotation)
        actual = self.pyom.get_and_free_c_str(ptr)
        expected = "http://biomodels.net/biology-qualifiers/is"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.singular_annotation_delete(singular_annotation)

    def test_singular_annotation_predicate_uri(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        singular_annotation = self.pyom.editor_new_singular_annotation(editor_ptr)
        self.pyom.singular_annotation_set_predicate_from_uri(singular_annotation,
                                                                 "https://predicate.com/from/uri".encode())
        ptr = self.pyom.singular_annotation_get_predicate(singular_annotation)
        actual = self.pyom.get_and_free_c_str(ptr)
        expected = "https://predicate.com/from/uri"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.singular_annotation_delete(singular_annotation)

    def test_singular_annotation_predicate_uri2(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        singular_annotation = self.pyom.editor_new_singular_annotation(editor_ptr)
        self.pyom.singular_annotation_predicate_from_uri(singular_annotation,
                                                                 "https://predicate.com/from/uri".encode())
        ptr = self.pyom.singular_annotation_get_predicate(singular_annotation)
        actual = self.pyom.get_and_free_c_str(ptr)
        expected = "https://predicate.com/from/uri"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.singular_annotation_delete(singular_annotation)

    def test_singular_annotation_resource_literal(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        singular_annotation = self.pyom.editor_new_singular_annotation(editor_ptr)
        self.pyom.singular_annotation_set_resource_literal(singular_annotation, "LiteralValue".encode())
        ptr = self.pyom.singular_annotation_get_resource(singular_annotation)
        actual = self.pyom.get_and_free_c_str(ptr)
        expected = "LiteralValue"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.singular_annotation_delete(singular_annotation)

    def test_singular_annotation_resource_literal2(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        singular_annotation = self.pyom.editor_new_singular_annotation(editor_ptr)
        self.pyom.singular_annotation_resource_literal(singular_annotation, "LiteralValue".encode())
        ptr = self.pyom.singular_annotation_get_resource(singular_annotation)
        actual = self.pyom.get_and_free_c_str(ptr)
        expected = "LiteralValue"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.singular_annotation_delete(singular_annotation)

    def test_singular_annotation_resource_uri(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        singular_annotation = self.pyom.editor_new_singular_annotation(editor_ptr)
        self.pyom.singular_annotation_set_resource_uri(singular_annotation, "UriValue".encode())
        ptr = self.pyom.singular_annotation_get_resource(singular_annotation)
        actual = self.pyom.get_and_free_c_str(ptr)
        expected = "UriValue"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.singular_annotation_delete(singular_annotation)


    def test_singular_annotation_resource_blank2(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        singular_annotation = self.pyom.editor_new_singular_annotation(editor_ptr)
        self.pyom.singular_annotation_resource_blank(singular_annotation, "blank".encode())
        ptr = self.pyom.singular_annotation_get_resource(singular_annotation)
        actual = self.pyom.get_and_free_c_str(ptr)
        expected = "blank"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.singular_annotation_delete(singular_annotation)

    def test_singular_annotation_str(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        singular_annotation = self.pyom.editor_new_singular_annotation(editor_ptr)
        self.pyom.singular_annotation_about(singular_annotation, "cytosol".encode())
        self.pyom.singular_annotation_set_predicate(singular_annotation, "bqbiol".encode(), "is".encode())
        self.pyom.singular_annotation_set_resource_uri(singular_annotation, "uniprot:PD12345".encode())

        self.pyom.editor_add_single_annotation(editor_ptr, singular_annotation)
        ptr = self.pyom.singular_annotation_str(
            singular_annotation, "turtle".encode())

        actual = self.pyom.get_and_free_c_str(ptr)
        print(actual)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#cytosol>
    bqbiol:is <https://identifiers.org/uniprot:PD12345> .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.singular_annotation_delete(singular_annotation)

    def test_editor_add_single_annotation(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        singular_annotation = self.pyom.editor_new_singular_annotation(editor_ptr)
        self.pyom.singular_annotation_about(singular_annotation, "https://uri.com#cytosol".encode())
        self.pyom.singular_annotation_set_predicate(singular_annotation, "bqbiol".encode(), "is".encode())
        self.pyom.singular_annotation_set_resource_uri(singular_annotation, "uniprot:PD12345".encode())
        self.pyom.editor_add_single_annotation(editor_ptr, singular_annotation)
        ptr = self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        actual = self.pyom.get_and_free_c_str(ptr)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<https://uri.com#cytosol>
    bqbiol:is <https://identifiers.org/uniprot:PD12345> .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.singular_annotation_delete(singular_annotation)


    def test_physical_entity_identity(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        physical_entity = self.pyom.editor_new_physical_entity(editor_ptr)
        self.pyom.physical_entity_identity(physical_entity, "uniprot:P456".encode())
        ptr = self.pyom.physical_entity_get_identity(physical_entity)
        actual = self.pyom.get_and_free_c_str(ptr)
        expected = "https://identifiers.org/uniprot:P456"
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_entity_delete(physical_entity)

    def test_physical_entity_num_locations(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        physical_entity = self.pyom.editor_new_physical_entity(editor_ptr)
        self.pyom.physical_entity_is_part_of(physical_entity, "fma:fma:3456".encode(), eUriType.IDENTIFIERS_URI)
        self.pyom.physical_entity_is_part_of(physical_entity, "fma/fma:3457".encode(), eUriType.IDENTIFIERS_URI)
        actual = self.pyom.physical_entity_get_num_locations(physical_entity)
        expected = 2
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_entity_delete(physical_entity)

    def test_physical_entity_is_part_of(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        physical_entity = self.pyom.editor_new_physical_entity(editor_ptr)
        self.pyom.physical_entity_is_part_of(physical_entity, "fma:3456".encode(), eUriType.IDENTIFIERS_URI)
        self.pyom.physical_entity_is_part_of(physical_entity, "fma:3457".encode(), eUriType.IDENTIFIERS_URI)
        num_locations = self.pyom.physical_entity_get_num_locations(physical_entity)
        ptr = [self.pyom.physical_entity_get_location(physical_entity, i) for i in range(num_locations)]
        actual = [self.pyom.get_and_free_c_str(i) for i in ptr]
        expected = ['https://identifiers.org/fma:3456', 'https://identifiers.org/fma:3457']
        self.assertEqual(expected, actual)
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_entity_delete(physical_entity)

    def test_physical_entity_sbml1(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        entity_property = self.pyom.editor_new_physical_property(editor_ptr)
        entity_property = self.pyom.physical_property_about(entity_property, "EntityProperty".encode(), eUriType.LOCAL_URI)
        entity_property = self.pyom.physical_property_is_version_of(entity_property, "opb:OPB_12345".encode())
        entity_property = self.pyom.physical_property_is_property_of(entity_property, "species0001".encode(), eUriType.MODEL_URI)

        physical_entity = self.pyom.editor_new_physical_entity(editor_ptr)
        physical_entity = self.pyom.physical_entity_about(physical_entity, "species0001".encode(), eUriType.LOCAL_URI)
        physical_entity = self.pyom.physical_entity_identity(physical_entity, "uniprot:PD12345".encode())
        physical_entity = self.pyom.physical_entity_is_part_of(physical_entity, "FMA:1234".encode(), eUriType.IDENTIFIERS_URI)
        physical_entity = self.pyom.physical_entity_has_property(physical_entity, entity_property)
        self.pyom.editor_add_physical_entity(editor_ptr, physical_entity)
        expected =  """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

local:EntityProperty
    bqbiol:isPropertyOf <http://omex-library.org/NewOmex.omex/NewModel.xml#species0001> ;
    bqbiol:isVersionOf <https://identifiers.org/opb:OPB_12345> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#species0001>
    bqbiol:is <https://identifiers.org/uniprot:PD12345> ;
    bqbiol:isPartOf <https://identifiers.org/FMA:1234> .""".encode()
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected, "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_entity_delete(physical_entity)
        self.pyom.physical_property_delete(entity_property)

    def test_physical_entity_sbml2(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)

        physical_entity = self.pyom.editor_new_physical_entity(editor_ptr)
        physical_entity = self.pyom.physical_entity_about(physical_entity, "species0001".encode(), eUriType.MODEL_URI)
        physical_entity = self.pyom.physical_entity_identity(physical_entity, "uniprot:PD12345".encode())
        physical_entity = self.pyom.physical_entity_is_part_of(physical_entity, "FMA:1234".encode(), eUriType.IDENTIFIERS_URI)
        physical_entity = self.pyom.physical_entity_has_property_full(
            physical_entity, "EntityProperty".encode(),
            eUriType.LOCAL_URI, "opb:OPB_12345".encode(),
            "species0001".encode(), eUriType.MODEL_URI)

        self.pyom.editor_add_physical_entity(editor_ptr, physical_entity)
        expected =  """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

local:EntityProperty
    bqbiol:isPropertyOf <http://omex-library.org/NewOmex.omex/NewModel.xml#species0001> ;
    bqbiol:isVersionOf <https://identifiers.org/opb:OPB_12345> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#species0001>
    bqbiol:is <https://identifiers.org/uniprot:PD12345> ;
    bqbiol:isPartOf <https://identifiers.org/FMA:1234> .""".encode()
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected, "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_entity_delete(physical_entity)

    def test_physical_entity_sbml3(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)

        physical_entity = self.pyom.editor_new_physical_entity(editor_ptr)
        physical_entity = self.pyom.physical_entity_about(physical_entity, "species0001".encode(), eUriType.MODEL_URI)
        physical_entity = self.pyom.physical_entity_identity(physical_entity, "uniprot:PD12345".encode())
        physical_entity = self.pyom.physical_entity_is_part_of(physical_entity, "FMA:1234".encode(), eUriType.IDENTIFIERS_URI)
        physical_entity = self.pyom.physical_entity_has_property_is_version_of(
            physical_entity, "opb:OPB_12345".encode())

        self.pyom.editor_add_physical_entity(editor_ptr, physical_entity)
        expected =  """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

local:EntityProperty0000
    bqbiol:isPropertyOf <http://omex-library.org/NewOmex.omex/NewModel.xml#species0001> ;
    bqbiol:isVersionOf <https://identifiers.org/opb:OPB_12345> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#species0001>
    bqbiol:is <https://identifiers.org/uniprot:PD12345> ;
    bqbiol:isPartOf <https://identifiers.org/FMA:1234> .""".encode()
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected, "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_entity_delete(physical_entity)

    def test_physical_entity_cellml1(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.cellml.encode(), True, False)
        entity_property = self.pyom.editor_new_physical_property(editor_ptr)
        entity_property = self.pyom.physical_property_about(entity_property, "main.Volume".encode(), eUriType.MODEL_URI)
        entity_property = self.pyom.physical_property_is_version_of(entity_property, "opb:OPB_00154".encode())
        entity_property = self.pyom.physical_property_is_property_of(entity_property, "entity0".encode(), eUriType.LOCAL_URI)

        physical_entity = self.pyom.editor_new_physical_entity(editor_ptr)
        physical_entity = self.pyom.physical_entity_about(physical_entity, "entity0".encode(), eUriType.LOCAL_URI)
        physical_entity = self.pyom.physical_entity_identity(physical_entity, "fma:9670".encode())
        physical_entity = self.pyom.physical_entity_is_part_of(physical_entity, "fma:18228".encode(), eUriType.IDENTIFIERS_URI)
        physical_entity = self.pyom.physical_entity_has_property(physical_entity, entity_property)
        self.pyom.editor_add_physical_entity(editor_ptr, physical_entity)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

local:entity0
    bqbiol:is <https://identifiers.org/fma:9670> ;
    bqbiol:isPartOf <https://identifiers.org/fma:18228> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#main.Volume>
    bqbiol:isPropertyOf local:entity0 ;
    bqbiol:isVersionOf <https://identifiers.org/opb:OPB_00154> .
""".encode()
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected, "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_entity_delete(physical_entity)
        self.pyom.physical_property_delete(entity_property)


    def test_physical_entity_cellml3(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.cellml.encode(), True, False)
        physical_entity = self.pyom.editor_new_physical_entity(editor_ptr)
        physical_entity = self.pyom.physical_entity_identity(physical_entity, "fma:9670".encode())
        physical_entity = self.pyom.physical_entity_is_part_of(physical_entity, "fma:18228".encode(), eUriType.IDENTIFIERS_URI)
        physical_entity = self.pyom.physical_entity_has_property_full(physical_entity,  "main.Volume".encode(), eUriType.MODEL_URI, "opb:OPB_00154".encode())
        self.pyom.editor_add_physical_entity(editor_ptr, physical_entity)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

local:Entity0000
    bqbiol:is <https://identifiers.org/fma:9670> ;
    bqbiol:isPartOf <https://identifiers.org/fma:18228> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#main.Volume>
    bqbiol:isPropertyOf local:Entity0000 ;
    bqbiol:isVersionOf <https://identifiers.org/opb:OPB_00154> .
""".encode()
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected, "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_entity_delete(physical_entity)

    def test_physical_process_sbml1(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        physical_process = self.pyom.editor_new_physical_process(editor_ptr)
        physical_process = self.pyom.physical_process_about(physical_process, "reaction0000".encode(), eUriType.MODEL_URI)
        physical_process = self.pyom.physical_process_add_source(physical_process, "species0000".encode(), eUriType.MODEL_URI, 1)
        physical_process = self.pyom.physical_process_add_sink(physical_process, "species0001".encode(), eUriType.MODEL_URI, 1)
        physical_process = self.pyom.physical_process_add_mediator(physical_process, "species0002".encode(), eUriType.MODEL_URI)
        physical_process = self.pyom.physical_process_has_property_full(
            physical_process, "ReactionProperty".encode(), eUriType.LOCAL_URI,
            "opb:OPB_00592".encode())
        self.pyom.editor_add_physical_process(editor_ptr, physical_process)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix semsim: <http://bime.uw.edu/semsim/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

local:MediatorParticipant0000
    semsim:hasPhysicalEntityReference <http://omex-library.org/NewOmex.omex/NewModel.xml#species0002> .

local:ReactionProperty
    bqbiol:isPropertyOf <http://omex-library.org/NewOmex.omex/NewModel.xml#reaction0000>  ;
    bqbiol:isVersionOf <https://identifiers.org/opb:OPB_00592> .

local:SinkParticipant0000
    semsim:hasMultiplier "1"^^rdf:double ;
    semsim:hasPhysicalEntityReference <http://omex-library.org/NewOmex.omex/NewModel.xml#species0001> .

local:SourceParticipant0000
    semsim:hasMultiplier "1"^^rdf:double ;
    semsim:hasPhysicalEntityReference <http://omex-library.org/NewOmex.omex/NewModel.xml#species0000> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#reaction0000>
    semsim:hasMediatorParticipant local:MediatorParticipant0000 ;
    semsim:hasSinkParticipant local:SinkParticipant0000 ;
    semsim:hasSourceParticipant local:SourceParticipant0000 .
""".encode()
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected, "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_process_delete(physical_process)

    def test_physical_process_sbml2(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        physical_process = self.pyom.editor_new_physical_process(editor_ptr)
        physical_process = self.pyom.physical_process_about(physical_process, "reaction0000".encode(), eUriType.MODEL_URI)
        physical_process = self.pyom.physical_process_add_source(physical_process, "species0000".encode(), eUriType.MODEL_URI, 1)
        physical_process = self.pyom.physical_process_add_sink(physical_process, "species0001".encode(), eUriType.MODEL_URI, 1)
        physical_process = self.pyom.physical_process_add_mediator(physical_process, "species0002".encode(), eUriType.MODEL_URI)
        physical_process = self.pyom.physical_process_has_property_is_version_of(physical_process, "opb:OPB_00592".encode())
        self.pyom.editor_add_physical_process(editor_ptr, physical_process)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix semsim: <http://bime.uw.edu/semsim/> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

local:MediatorParticipant0000
    semsim:hasPhysicalEntityReference <http://omex-library.org/NewOmex.omex/NewModel.xml#species0002> .

local:ProcessProperty0000
    bqbiol:isPropertyOf <http://omex-library.org/NewOmex.omex/NewModel.xml#reaction0000> ;
    bqbiol:isVersionOf <https://identifiers.org/opb:OPB_00592> .

local:SinkParticipant0000
    semsim:hasMultiplier "1"^^rdf:double ;
    semsim:hasPhysicalEntityReference <http://omex-library.org/NewOmex.omex/NewModel.xml#species0001> .

local:SourceParticipant0000
    semsim:hasMultiplier "1"^^rdf:double ;
    semsim:hasPhysicalEntityReference <http://omex-library.org/NewOmex.omex/NewModel.xml#species0000> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#reaction0000>
    semsim:hasMediatorParticipant local:MediatorParticipant0000 ;
    semsim:hasSinkParticipant local:SinkParticipant0000 ;
    semsim:hasSourceParticipant local:SourceParticipant0000 .
""".encode()
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected, "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_process_delete(physical_process)

    def test_physical_process_cellml1(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.cellml.encode(), True, False)
        physical_process = self.pyom.editor_new_physical_process(editor_ptr)
        physical_process = self.pyom.physical_process_about(physical_process, "Process".encode(), eUriType.LOCAL_URI)
        physical_process = self.pyom.physical_process_add_source(physical_process, "entity1".encode(), eUriType.LOCAL_URI, 1)
        physical_process = self.pyom.physical_process_add_sink(physical_process, "entity2".encode(), eUriType.LOCAL_URI, 1)
        physical_process = self.pyom.physical_process_add_mediator(physical_process, "entity3".encode(), eUriType.LOCAL_URI)
        physical_process = self.pyom.physical_process_has_property_full(
            physical_process, "main.ReactionRate".encode(), eUriType.MODEL_URI,
            "opb:OPB_00592".encode(), "Process".encode(), eUriType.LOCAL_URI)
        self.pyom.editor_add_physical_process(editor_ptr, physical_process)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix semsim: <http://bime.uw.edu/semsim/> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

local:MediatorParticipant0000
    semsim:hasPhysicalEntityReference local:entity3 .

local:Process
    semsim:hasMediatorParticipant local:MediatorParticipant0000 ;
    semsim:hasSinkParticipant local:SinkParticipant0000 ;
    semsim:hasSourceParticipant local:SourceParticipant0000 .

local:SinkParticipant0000
    semsim:hasMultiplier "1"^^rdf:double ;
    semsim:hasPhysicalEntityReference local:entity2 .

local:SourceParticipant0000
    semsim:hasMultiplier "1"^^rdf:double ;
    semsim:hasPhysicalEntityReference local:entity1 .

<http://omex-library.org/NewOmex.omex/NewModel.xml#main.ReactionRate>
    bqbiol:isPropertyOf local:Process ;
    bqbiol:isVersionOf <https://identifiers.org/opb:OPB_00592> .
""".encode()
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected, "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_process_delete(physical_process)

    def test_physical_process_cellml2(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.cellml.encode(), True, False)
        physical_process = self.pyom.editor_new_physical_process(editor_ptr)
        physical_process = self.pyom.physical_process_add_source(physical_process, "entity1".encode(), eUriType.LOCAL_URI, 1)
        physical_process = self.pyom.physical_process_add_sink(physical_process, "entity2".encode(), eUriType.LOCAL_URI, 1)
        physical_process = self.pyom.physical_process_add_mediator(physical_process, "entity3".encode(), eUriType.LOCAL_URI)
        physical_process = self.pyom.physical_process_has_property_full(
            physical_process, "main.Volume".encode(), eUriType.MODEL_URI,
            "opb:OPB_00592".encode())
        self.pyom.editor_add_physical_process(editor_ptr, physical_process)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix semsim: <http://bime.uw.edu/semsim/> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

local:MediatorParticipant0000
    semsim:hasPhysicalEntityReference local:entity3 .

local:Process0000
    semsim:hasMediatorParticipant local:MediatorParticipant0000 ;
    semsim:hasSinkParticipant local:SinkParticipant0000 ;
    semsim:hasSourceParticipant local:SourceParticipant0000 .

local:SinkParticipant0000
    semsim:hasMultiplier "1"^^rdf:double ;
    semsim:hasPhysicalEntityReference local:entity2 .

local:SourceParticipant0000
    semsim:hasMultiplier "1"^^rdf:double ;
    semsim:hasPhysicalEntityReference local:entity1 .

<http://omex-library.org/NewOmex.omex/NewModel.xml#main.Volume>
    bqbiol:isPropertyOf local:Process0000 ;
    bqbiol:isVersionOf <https://identifiers.org/opb:OPB_00592> .
""".encode()
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected, "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.physical_process_delete(physical_process)

    def test_energy_diff_sbml1(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        energy_diff = self.pyom.editor_new_energy_diff(editor_ptr)
        energy_diff = self.pyom.energy_diff_about(energy_diff, "reaction0000".encode(), eUriType.MODEL_URI)
        energy_diff = self.pyom.energy_diff_add_source(energy_diff, "species0001".encode(), eUriType.MODEL_URI)
        energy_diff = self.pyom.energy_diff_add_sink(energy_diff, "species0002".encode(), eUriType.MODEL_URI)
        energy_diff = self.pyom.energy_diff_has_property_full(
            energy_diff, "parameter_metaid_0".encode(), eUriType.LOCAL_URI, "opb:OPB_01058".encode(), "EnergyDiff_0".encode(), eUriType.MODEL_URI)
        self.pyom.editor_add_energy_diff(editor_ptr, energy_diff)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix semsim: <http://bime.uw.edu/semsim/> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

local:SinkParticipant0000
    semsim:hasPhysicalEntityReference <http://omex-library.org/NewOmex.omex/NewModel.xml#species0002> .

local:SourceParticipant0000
    semsim:hasPhysicalEntityReference <http://omex-library.org/NewOmex.omex/NewModel.xml#species0001> .

local:parameter_metaid_0
    bqbiol:isPropertyOf <http://omex-library.org/NewOmex.omex/NewModel.xml#reaction0000> ;
    bqbiol:isVersionOf <https://identifiers.org/opb:OPB_01058> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#reaction0000>
    semsim:hasSinkParticipant local:SinkParticipant0000 ;
    semsim:hasSourceParticipant local:SourceParticipant0000 .
""".encode()
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected, "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.energy_diff_delete(energy_diff)

    def test_energy_diff_sbml2(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        energy_diff = self.pyom.editor_new_energy_diff(editor_ptr)
        energy_diff = self.pyom.energy_diff_about(energy_diff, "reaction0000".encode(), eUriType.MODEL_URI)
        energy_diff = self.pyom.energy_diff_add_source(energy_diff, "species0000".encode(), eUriType.MODEL_URI)
        energy_diff = self.pyom.energy_diff_add_sink(energy_diff, "species0001".encode(), eUriType.MODEL_URI)
        energy_diff = self.pyom.energy_diff_has_property_is_version_of(
            energy_diff, "opb:OPB_01058".encode()
        )
        self.pyom.editor_add_energy_diff(editor_ptr, energy_diff)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix semsim: <http://bime.uw.edu/semsim/> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

local:EnergyDiffProperty0000
    bqbiol:isPropertyOf <http://omex-library.org/NewOmex.omex/NewModel.xml#reaction0000> ;
    bqbiol:isVersionOf <https://identifiers.org/opb:OPB_01058> .

local:SinkParticipant0000
    semsim:hasPhysicalEntityReference <http://omex-library.org/NewOmex.omex/NewModel.xml#species0001> .

local:SourceParticipant0000
    semsim:hasPhysicalEntityReference <http://omex-library.org/NewOmex.omex/NewModel.xml#species0000> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#reaction0000>
    semsim:hasSinkParticipant local:SinkParticipant0000 ;
    semsim:hasSourceParticipant local:SourceParticipant0000 .
""".encode()
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected, "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.energy_diff_delete(energy_diff)

    def test_energy_diff_cellml1(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.cellml.encode(), True, False)
        energy_diff = self.pyom.editor_new_energy_diff(editor_ptr)
        energy_diff = self.pyom.energy_diff_about(energy_diff, "main.MembraneVoltage".encode(),
                                                                          eUriType.MODEL_URI)
        energy_diff = self.pyom.energy_diff_add_source(energy_diff, "entity1".encode(),
                                                                 eUriType.MODEL_URI)
        energy_diff = self.pyom.energy_diff_add_sink(energy_diff, "entity2".encode(),
                                                               eUriType.MODEL_URI)
        energy_diff = self.pyom.energy_diff_has_property_full(
            energy_diff, "EnergyDiffProperty".encode(), eUriType.MODEL_URI, "opb:OPB_00592".encode(), "main.MembraneVoltage".encode(), eUriType.MODEL_URI)
        self.pyom.editor_add_energy_diff(editor_ptr, energy_diff)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix bqbiol: <http://biomodels.net/biology-qualifiers/> .
@prefix semsim: <http://bime.uw.edu/semsim/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

local:SinkParticipant0000
    semsim:hasPhysicalEntityReference <http://omex-library.org/NewOmex.omex/NewModel.xml#entity2> .

local:SourceParticipant0000
    semsim:hasPhysicalEntityReference <http://omex-library.org/NewOmex.omex/NewModel.xml#entity1> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#EnergyDiffProperty>
    bqbiol:isPropertyOf <http://omex-library.org/NewOmex.omex/NewModel.xml#main.MembraneVoltage> ;
    bqbiol:isVersionOf <https://identifiers.org/opb:OPB_00592> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#main.MembraneVoltage>
    semsim:hasSinkParticipant local:SinkParticipant0000 ;
    semsim:hasSourceParticipant local:SourceParticipant0000 .

""".encode()
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected, "turtle".encode()))
        self.pyom.editor_delete(editor_ptr)
        self.pyom.energy_diff_delete(energy_diff)

    def test_personal_information_new(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        information = self.pyom.editor_new_personal_information(editor_ptr)
        self.pyom.personal_information_delete(information)
        self.pyom.editor_delete(editor_ptr)
        self.assertTrue(True)  # if we get this far we pass. Bad test but who's counting

    def test_personal_get_local_uri(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        information = self.pyom.editor_new_personal_information(editor_ptr)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.personal_information_get_local_uri(information)
        )
        expected = "http://omex-library.org/NewOmex.omex/NewModel.rdf#"
        self.assertEqual(expected, actual)
        self.pyom.personal_information_delete(information)
        self.pyom.editor_delete(editor_ptr)

    def test_personal_information_add_creator(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        information = self.pyom.editor_new_personal_information(editor_ptr)
        self.pyom.personal_information_add_creator(information, "1234-1234-1234-1234".encode())
        self.pyom.editor_add_personal_information(editor_ptr, information)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        )
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dc: <https://dublincore.org/specifications/dublin-core/dcmi-terms/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    dc:creator <http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000>
    dc:creator <https://identifiers.org/orcid/1234-1234-1234-1234> .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.personal_information_delete(information)
        self.pyom.editor_delete(editor_ptr)

    def test_personal_information_add_name(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        information = self.pyom.editor_new_personal_information(editor_ptr)
        self.pyom.personal_information_add_name(information, "Ciaran Welsh".encode())
        self.pyom.editor_add_personal_information(editor_ptr, information)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        )
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dc: <https://dublincore.org/specifications/dublin-core/dcmi-terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    dc:creator <http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000>
    foaf:name "Ciaran Welsh"^^rdf:string .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.personal_information_delete(information)
        self.pyom.editor_delete(editor_ptr)

    def test_personal_information_add_mbox(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        information = self.pyom.editor_new_personal_information(editor_ptr)
        self.pyom.personal_information_add_mbox(information, "annotations.uw.edu".encode())
        self.pyom.editor_add_personal_information(editor_ptr, information)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        )
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dc: <https://dublincore.org/specifications/dublin-core/dcmi-terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    dc:creator <http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000>
    foaf:mbox "annotations.uw.edu"^^rdf:string .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.personal_information_delete(information)
        self.pyom.editor_delete(editor_ptr)

    def test_personal_information_add_account_name(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        information = self.pyom.editor_new_personal_information(editor_ptr)
        self.pyom.personal_information_add_account_name(information, "1234-1234-1234-1234".encode())
        self.pyom.editor_add_personal_information(editor_ptr, information)
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dc: <https://dublincore.org/specifications/dublin-core/dcmi-terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    dc:creator <http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000>
    foaf:accountName <https://orcid.org/1234-1234-1234-1234> .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.personal_information_delete(information)
        self.pyom.editor_delete(editor_ptr)

    def test_personal_information_add_account_service_homepage(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        information = self.pyom.editor_new_personal_information(editor_ptr)
        self.pyom.personal_information_add_account_service_homepage(
            information,
            "https://github.com/sys-bio/libOmexMeta".encode()
        )
        self.pyom.editor_add_personal_information(editor_ptr, information)

        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dc: <https://dublincore.org/specifications/dublin-core/dcmi-terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    dc:creator <http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000>
    foaf:accountServiceHomepage <https://github.com/sys-bio/libOmexMeta> .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.personal_information_delete(information)
        self.pyom.editor_delete(editor_ptr)

    def test_personal_information_add_foaf_blank(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        information = self.pyom.editor_new_personal_information(editor_ptr)
        self.pyom.personal_information_add_foaf_blank(information, "name".encode(), "Blank".encode())
        self.pyom.editor_add_personal_information(editor_ptr, information)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        )
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dc: <https://dublincore.org/specifications/dublin-core/dcmi-terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    dc:creator <http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000>
    foaf:name _:Blank .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.personal_information_delete(information)
        self.pyom.editor_delete(editor_ptr)

    def test_personal_information_add_foaf_uri(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        information = self.pyom.editor_new_personal_information(editor_ptr)
        self.pyom.personal_information_add_foaf_uri(information, "mbox".encode(), "http://uri.com/".encode())
        self.pyom.editor_add_personal_information(editor_ptr, information)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        )
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dc: <https://dublincore.org/specifications/dublin-core/dcmi-terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    dc:creator <http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000>
    foaf:mbox <http://uri.com/> .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.personal_information_delete(information)
        self.pyom.editor_delete(editor_ptr)

    def test_personal_information_add_foaf_literal(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        information = self.pyom.editor_new_personal_information(editor_ptr)
        self.pyom.personal_information_add_foaf_literal(information, "name".encode(), "literal".encode())
        self.pyom.editor_add_personal_information(editor_ptr, information)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.rdf_to_string(self.rdf, "turtle".encode())
        )
        expected = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dc: <https://dublincore.org/specifications/dublin-core/dcmi-terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix OMEXlib: <http://omex-library.org/> .
@prefix myOMEX: <http://omex-library.org/NewOmex.omex/> .
@prefix local: <http://omex-library.org/NewOmex.omex/NewModel.rdf#> .

<http://omex-library.org/NewOmex.omex/NewModel.xml>
    dc:creator <http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000> .

<http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000>
    foaf:name "literal"^^rdf:string .

"""
        self.assertTrue(self.pyom.rdf_equals_rdf_vs_string(self.rdf, expected.encode(), "turtle".encode()))
        self.pyom.personal_information_delete(information)
        self.pyom.editor_delete(editor_ptr)

    def test_personal_information_get_metaid(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        information = self.pyom.editor_new_personal_information(editor_ptr)
        self.pyom.editor_add_personal_information(editor_ptr, information)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.personal_information_get_metaid(information)
        )
        expected = "http://omex-library.org/NewOmex.omex/NewModel.xml#PersonalInfo0000"
        self.assertEqual(expected, actual)
        self.pyom.personal_information_delete(information)
        self.pyom.editor_delete(editor_ptr)

    def test_personal_information_get_model_uri(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        information = self.pyom.editor_new_personal_information(editor_ptr)
        self.pyom.editor_add_personal_information(editor_ptr, information)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.personal_information_get_model_uri(information)
        )
        expected = "http://omex-library.org/NewOmex.omex/NewModel.xml"
        self.assertEqual(expected, actual)
        self.pyom.personal_information_delete(information)
        self.pyom.editor_delete(editor_ptr)

    def test_personal_information_set_model_uri(self):
        editor_ptr = self.pyom.rdf_to_editor(self.rdf, TestStrings.xml.encode(), True, False)
        information = self.pyom.editor_new_personal_information(editor_ptr)
        self.pyom.personal_information_set_model_uri(information, "awesome-model.xml".encode())
        self.pyom.editor_add_personal_information(editor_ptr, information)
        actual = self.pyom.get_and_free_c_str(
            self.pyom.personal_information_get_model_uri(information)
        )
        expected = "awesome-model.xml"
        self.assertEqual(expected, actual)
        self.pyom.personal_information_delete(information)
        self.pyom.editor_delete(editor_ptr)


if __name__ == "__main__":
    unittest.main()
