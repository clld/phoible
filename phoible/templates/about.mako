<%inherit file="home_comp.mako"/>

<h3>Overview</h3>

<p>The current database includes roughly:</p>
<ul>
<li>200 languages' phonemic and corresponding allophonic inventories from the Stanford Phonology Archive (SPA; Crothers et al, 1979)</li>
<li>451 languages' phonemic inventories from the UCLA Phonological Segment Inventory Database (UPSID; Maddieson 1984, Maddieson &amp; Precoda 1990)</li>
<li>200 African languages' phonemic inventories (Hartell 1993, Chanard 2006)</li>
<li>and hundreds of other inventories, including descriptions of phonemes, allophones and their conditioning environments, which we extracted from secondary resources like grammars and phonological descriptions</li>
</ul>

<p>The data set also includes additional genealogical and geographical information about each language.</p>

<p>The PHOIBLE project also integrates the theoretical model of distinctive features from an extended phonological feature set based on International Phonetic Alphabet (IPA; International Phonetic Association 2005) and on Hayes 2009. This is accomplished by creating a mapping relationship from each IPA segment to a set of features (Moran 2012). In this way, the IPA is a pivot for interoperability across all resources in PHOIBLE because their contents are encoded in Unicode IPA.</p>

<p>For a detailed description of PHOIBLE, see
    ${h.external_link("https://digital.lib.washington.edu/researchworks/handle/1773/22452", label="Moran 2012a")}.
    For examples of some of the research we are doing with PHOIBLE, see:
    ${h.external_link("http://dx.doi.org/10.1353/lan.2012.0087", label="Moran, McCloy & Wright 2012")},
    Cysouw, Dediu &amp; Moran 2012,
    McCloy, Moran &amp; Wright 2013
    and Moran &amp; Blasi, forthcoming.
</p>

<h3>Downloadable data</h3>
<p>
    PHOIBLE was funded in 2009 by a grant from the Royalty Research Fund at the University of Washington. The data are available
    in several formats for research purposes only. For commercial use,
    <a href="mailto:phoible@uw.edu">contact us</a>.
    If you use the data in a publication, please include the appropriate citation. (Notify us and we'll add you to the PHOIBLE bibliography.)
</p>
<ul>
    <li>
        <a href="${request.static_url('phoible:static/data/MoranEtAl2012_rawData.tab')}">Raw supplemental data</a> for: <em>Revisiting population size vs. phoneme inventory size</em>.</li>
    <li>
        <a href="${request.static_url('phoible:static/data/MoranEtAl2012_phonemeData.tab')}">Phoneme level supplemental data</a> for: <em>Revisiting population size vs. phoneme inventory size</em>.
        <ul>
            <li>
                Moran, Steven, Daniel McCloy and Richard Wright. 2012. Revisiting population size vs. phoneme inventory size.
                <em>Language</em>, 88(4), 877-893.
                ${h.external_link("http://dx.doi.org/10.1353/lan.2012.0087", label="doi:10.1353/lan.2012.0087")}
                (${h.external_link("http://students.washington.edu/drmccloy/pubs/MoranMcCloyWright2012_revWebVersion.pdf", label="Pre-publication manuscript")} | <a href="${request.static_url('phoible:static/data/MoranMcCloyWright2012.bib')}">BibTeX</a>)
            </li>
        </ul>
    </li>
    <li>
        <a href="${request.static_url('phoible:static/data/Moran2012_phonemeData.xml')}" target="_blank">PHOIBLE phoneme level MySQL dump (XML)</a>
        <ul>
            <li>
                Moran, Steven. 2012a. Phonetics Information Base and Lexicon. PhD thesis, University of Washington.
                ${h.external_link("https://digital.lib.washington.edu/researchworks/handle/1773/22452")}.
                (<a href="${request.static_url('phoible:static/data/Moran2012_10_page_diss_abstract.pdf')}">10 page dissertation abstract</a> | <a href="${request.static_url('phoible:static/data/Moran2012a.bib')}">BibTeX</a>)
            </li>
        </ul>
    </li>
    <li>
        PHOIBLE RDF Linked Data for the
        ${h.external_link("http://linguistics.okfn.org/resources/llod/", label="LLOD")}.
        <ul>
            <li>
                Moran, Steven. 2012b. Using Linked Data to Create a Typological Knowledge Base.
                In Linked Data in Linguistics: Representing and Connecting Language Data and Language Metadata, Christian Chiarcos, Sebastian Nordhoff and Sebastian Hellmann (eds). Springer, Heidelberg.
                (<a href="${request.static_url('phoible:static/data/Moran2012b.bib')}">BibTeX</a>)
            </li>
        </ul>
    </li>
    <li>
        ${h.external_link("http://www.sciencemag.org/content/suppl/2012/02/09/335.6069.657-b.DC1/Cysouw.SOM.pdf", label="Supplemental material")} for:
        <em>Still No Evidence for an Ancient Language Expansion From Africa</em>.
    </li>
    <li>
        <ul>
            <li>
                Cysouw, Michael and Dan Dediu and Steven Moran. 2012. Still No Evidence for an Ancient Language Expansion From Africa.
                <em>Science</em>, 355: 657--b.
                (${h.external_link("http://www.sciencemag.org/content/335/6069/657.2.full", label="Full paper")} | <a href="${request.static_url('phoible:static/data/CysouwDediuMoran.bib')}">BibTeX</a>)
            </li>
        </ul>
    </li>
</ul>

<h3>References</h3>
<ul>
    <li>Chanard, Christian. 2006. Syst&egrave;mes Alphab&eacute;tiques des langues africaines. Online: ${h.external_link("http://sumale.vjf.cnrs.fr/phono/")}.</li>
    <!-- <li>Chomsky, Noam and Morris Halle. 1968. The Sound Pattern of English. Harper &amp; Row.</li> -->
    <li>Crothers, John H., James P. Lorentz, Donald A. Sherman and Marilyn M. Vihman. 1979. Handbook of Phonological Data From a Sample of the World's Languages: A Report of the Stanford Phonology Archive.</li>
    <li>Cysouw, Michael and Dan Dediu and Steven Moran. 2012. Still No Evidence for an Ancient Language Expansion From Africa. <em>Science</em>, 355: 657--b.</li>
    <li>Hartell, Rhonda L. 1993. Alphabets des langues africaines. UNESCO and Soci&eacute;t&eacute; Internationale de Linguistique.</li>
    <li>Hayes, Bruce. 2009. Introductory Phonology. Blackwell.</li>
    <li>International Phonetic Association. 2005. International Phonetic Alphabet. ${h.external_link("http://www.arts.gla.ac.uk/IPA/")}.</li>
    <!-- <li>Jakobson, Roman. 1939. Observations sur le classment phonologique des consonnes. In Proceedings of the 3rd International Conference of Phonetic Sciences, 34-41.</li> -->
    <!-- <li>Jakobson, Roman, Gunnar Fant and Morris Halle. 1952. Preliminaries to Speech Analysis. MIT Press.</li> -->
    <!-- <li>Krauss, Michael. 1992. The World's Languages in Crisis. Language, 68(1), 4-10.</li> -->
    <li>Maddieson, Ian and Kristin Precoda. 1990. Updating UPSID. In UCLA Working Papers in Phonetics, 74, 104-111.</li>
    <li>Maddieson, Ian. 1984. Pattern of Sounds. Cambridge University Press.</li>
    <li>McCloy, Daniel, Steven Moran and Richard Wright. 2013. Revisiting ‘The role of features in phonological inventories’. Paper presented at the CUNY Conference on the Feature in Phonology and Phonetics. (<a href="http://students.washington.edu/drmccloy/pubs/McCloyEtAl2013_cunyFeatureConf.pdf" target="_blank">Slides</a> | <a href="http://students.washington.edu/drmccloy/pubs/refs/McCloyEtAl2013_cunyFeatureConf.bib" target="_blank">BibTeX</a>)</li>
    <li>
        Moran, Steven. 2012a. ${h.external_link("https://digital.lib.washington.edu/researchworks/handle/1773/22452", label="Phonetics Information Base and Lexicon")}.
        PhD thesis. University of Washington.
    </li>
    <li>Moran, Steven. 2012b. Using Linked Data to Create a Typological Knowledge Base. In Linked Data in Linguistics: Representing and Connecting Language Data and Language Metadata, Christian Chiarcos, Sebastian Nordhoff and Sebastian Hellmann (eds). Springer, Heidelberg.</li>
    <li>Moran, Steven and Damian Blasi. Forthcoming. Cross-linguistic comparison of complexity measures in phonological systems.</li>
    <li>Moran, Steven, Daniel McCloy and Richard Wright. 2012.
    ${h.external_link("http://dx.doi.org/10.1353/lan.2012.0087", label="Revisiting Population Size vs. Phoneme Inventory Size")}. <em>Language</em>, 88(4), 877-893.</li>
    <!-- <li>Trubetzkoy, Nikolai. 1939. Grundz&#252;ge der Phonologie. Travaux du cercle linguistique de Prague 7.</li> -->
    <li>The above references in <a href="${request.static_url('phoible:static/data/phoible.bib')}" target="_blank">BibTeX</a>.</li>
</ul>