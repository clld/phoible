<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

<%def name="sidebar()">
    <%util:well title="Cite">
        ${h.newline2br(h.text_citation(request, ctx))|n}
        ${h.cite_button(request, ctx)}
    </%util:well>
</%def>

<h2>Welcome to PHOIBLE</h2>

<p>PHOIBLE is a repository of cross-linguistic phonological inventory data, which have been extracted from source
    documents and tertiary databases and compiled into a single searchable convenience sample. Release 2.0 from 2019
    includes ${inventory_count} inventories that contain ${segment_count} segment types found in ${language_count}
    distinct languages.</p>

<p>A bibliographic record is provided for each source document; note that some languages in PHOIBLE have multiple
    entries based on distinct sources that disagree about the number and/or identity of that language’s phonemes.</p>

<p>Two principles guide the development of PHOIBLE, though it has proved challenging both theoretically and
    technologically to abide by them:</p>

<ol>
    <li>Be faithful to the language description in the source document (now often called ‘doculect’, for reasons
        indicated above)
    </li>
    <li>Encode all character data in a consistent representation in Unicode IPA</li>
</ol>

<p>In addition to phoneme inventories, PHOIBLE includes distinctive feature data for every phoneme in every language.
    The feature system used was created by the PHOIBLE developers to be descriptively adequate cross-linguistically. In
    other words, if two phonemes differ in their graphemic representation, then they necessarily differ in their
    featural representation as well (regardless of whether those two phonemes coexist in any known doculect). The
    feature system is loosely based on the feature system in
    ${h.link(request, sources['Hayes2009'], label="Hayes 2009")} with some additions drawn
    from ${h.link(request, sources['MoisikEsling2011'], label="Moisik & Esling 2011")}.
</p>

<p>However, the final feature system goes beyond both of these sources, and is potentially subject to change as new
    languages are added in subsequent editions of PHOIBLE.</p>

##<p>The 2014 edition includes inventories from the following contributors:</p>
##<%util:table args="item" options="${dict(bFilter=False)}" items="${[c for c in contributors if c.contribution_assocs]}" class_="table-nonfluid table-striped">
##    <%def name="head()">
##        <th>Contributor</th>
##        <th>Description</th>
##        <th>Sources</th>
##        <th>Number of inventories</th>
##    </%def>
##    <td>${item.name} (${item.id})</td>
##    <td>${descriptions[item.id]|n}</td>
##    <td>
##        <ul class="unstyled inline">
##            % for ref in item.references:
##            <li>${h.link(request, ref.source)}</li>
##            % endfor
##        </ul>
##    </td>
##    <td class="right">${len(item.contribution_assocs)}</td>
##</%util:table>

<p>The data set also includes additional genealogical and geographical information about each language from
    ${h.external_link('https://glottolog.org', label='Glottolog')}.</p>

<p>
    The PHOIBLE project also integrates the theoretical model of distinctive features from
    an extended phonological feature set based on International Phonetic Alphabet
    (${h.link(request, sources['IPA2005'])}) and on ${h.link(request, sources['Hayes2009'])}.
    This is accomplished by creating a mapping relationship from each IPA segment to a set
    of features (${h.link(request, sources['Moran2012a'])}). In this way, the IPA is a pivot for interoperability across
    all resources in PHOIBLE because their contents are encoded in Unicode IPA.
</p>

<p>For a detailed description of PHOIBLE, see
    ${h.link(request, sources['Moran2012a'])}.
    For examples of some of the research we are doing with PHOIBLE, see:

    ${h.link(request, sources['Moran_etal2012'])},
    ${h.link(request, sources['Cysouw_etal2012'])},
    ${h.link(request, sources['mccloy_etal2013'])}
    and Moran &amp; Blasi, Cross-linguistic comparison of complexity measures in phonological systems, forthcoming.
</p>


<h3>How to use PHOIBLE</h3>

<p>Users can browse or search PHOIBLE's inventories by clicking on the tabs <a
        href="${request.route_url('contributions')}">"Inventories"</a>, <a href="${request.route_url('languages')}">"Languages"</a>
    or <a href="${request.route_url('parameters')}">"Segments"</a> above. Data can be downloaded by clicking the
    download button <i class="icon icon-download-alt"> </i>. If you use PHOIBLE in your research, please cite
    appropriately, following our recommended citation format.</p>


<h3>How to cite PHOIBLE</h3>

<p>If you are citing the database as a whole, or making use of the phonological distinctive feature systems in PHOIBLE,
    please cite as follows:</p>

<%util:well>
    ${h.newline2br(h.text_citation(request, ctx))|n}
    ${h.cite_button(request, ctx)}
    <a href="https://doi.org/10.5281/zenodo.2593234"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.2593234.svg" alt="DOI"></a>
</%util:well>

<p>If you are citing phoneme inventory data for a particular language or languages, please use the name of the language
    as the title, and include the original data source as an element within PHOIBLE:<p>

        <%util:well>
        ${h.newline2br(h.text_citation(request, h.models.Contribution.get("441")))|n}
        ${h.cite_button(request, h.models.Contribution.get("441"))}
    </%util:well>
