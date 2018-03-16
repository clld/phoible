<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>

<h3>Downloadable data</h3>

<p>
    In addition to the various data formats available for single resources or tables of
    PHOIBLE
    by clicking the download buttons <i class="icon-download-alt"> </i> on the resource's
    pages,
    we provide some bulk downloads of PHOIBLE data.
</p>
<ul>
    <li>
        The data of PHOIBLE is aggregated from
        ${h.external_link('https://github.com/phoible/phoible/releases/tag/v2014', 'release v2014')}
        of the raw data curated in a
        ${h.external_link('https://github.com/phoible/phoible', 'GitHub repository')}.
    </li>
    <li>
        A full dump of the database in
        ${h.external_link('http://www.w3.org/RDF/', 'RDF')}
        serialized as
        ${h.external_link('http://en.wikipedia.org/wiki/Notation3', 'N3')}
        is available here: <a
            href="https://cdstar.shh.mpg.de/bitstreams/EAEA0-DAEC-55A7-3896-0/phoible_dataset.n3.gz">RDF dump</a>
    </li>
    <li>
        An export of the database in
        ${h.external_link('http://cldf.clld.org', 'CLDF')}
        is available here: <a
            href="https://cdstar.shh.mpg.de/bitstreams/EAEA0-BE27-DAC8-9268-0/phoible_dataset.cldf.zip">PHOIBLE CLDF 1.0</a>
    </li>
    <li>
        Supplemental data for the paper
        <br/>
        Moran, Steven, Daniel McCloy and Richard Wright. 2012. Revisiting population size
        vs. phoneme inventory size.
        <em>Language</em>, 88(4), 877-893.
        <a href="http://dx.doi.org/10.1353/lan.2012.0087"
           title="doi:10.1353/lan.2012.0087"><i class="icon-share"></i>
            doi:10.1353/lan.2012.0087</a>
        <ul>
            <li>
                <a href="/static/data/MoranMcCloyWright2012.bib">BibTeX</a>
            </li>
            <li>
                <a href="/static/data/MoranEtAl2012_rawData.tab">raw supplemental data</a>,
            </li>
            <li>
                <a href="/static/data/MoranEtAl2012_phonemeData.tab">phoneme level
                    supplemental data</a>.
            </li>
        </ul>
    </li>
</ul>

<p>Please cite PHOIBLE as follows:</p>

<%util:well>
    ${h.newline2br(h.text_citation(request, request.dataset))|n}
    ${h.cite_button(request, request.dataset)}
</%util:well>
