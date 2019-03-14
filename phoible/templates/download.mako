<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>

<h3>Downloadable data</h3>

<p>
    In addition to the various data formats available for single resources or tables of PHOIBLE
    by clicking the download buttons <i class="icon-download-alt"> </i> on the resource's
    pages, a bulk download of PHOIBLE data as ${h.external_link('https://cldf.clld.org', label='CLDF')}
    StructureDataset is available at ZENODO:<br>
    <a href="https://doi.org/10.5281/zenodo.2593234"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.2593234.svg"
                                                          alt="DOI"></a>
</p>

<p>
    The data of PHOIBLE is curated in a
    ${h.external_link('https://github.com/phoible/phoible', 'GitHub repository')}.
</p>

<p>
    Supplemental data for the paper
</p>
<blockquote>
    Moran, Steven, Daniel McCloy and Richard Wright. 2012. Revisiting population size
    vs. phoneme inventory size.
    <em>Language</em>, 88(4), 877-893.
    <a href="http://dx.doi.org/10.1353/lan.2012.0087"
       title="doi:10.1353/lan.2012.0087"><i class="icon-share"></i>
        doi:10.1353/lan.2012.0087</a>

</blockquote>
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
</p>

<p>Please cite PHOIBLE as follows:</p>

<%util:well>
    ${h.newline2br(h.text_citation(request, request.dataset))|n}
    ${h.cite_button(request, request.dataset)}
    <a href="https://doi.org/10.5281/zenodo.2593234"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.2593234.svg"
                                                          alt="DOI"></a>
</%util:well>

<h4>Earlier versions of PHOIBLE</h4>
<p>
    Previous released versions of PHOIBLE are archived with and available from ZENODO:
    ${h.external_link('https://doi.org/10.5281/zenodo.2562766', label='DOI 10.5281/zenodo.2562766')}.
</p>
