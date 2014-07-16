<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>

<h3>Overview</h3>

<p>The current database includes inventories from the following contributors:</p>
<%util:table args="item" options="${dict(bFilter=False)}" items="${[c for c in contributors if c.contribution_assocs]}" class_="table-nonfluid table-striped">
    <%def name="head()">
        <th> </th>
        <th>Contributor</th>
        <th>Sources</th>
        <th>Number of inventories</th>
    </%def>
    <td>${item.id}</td>
    <td>${item.name}</td>
    <td>
        <ul class="unstyled inline">
            % for ref in item.references:
            <li>${h.link(request, ref.source)}</li>
            % endfor
        </ul>
    </td>
    <td class="right">${len(item.contribution_assocs)}</td>
</%util:table>

<p>The data set also includes additional genealogical and geographical information about each language.</p>

<p>
    The PHOIBLE project also integrates the theoretical model of distinctive features from
    an extended phonological feature set based on International Phonetic Alphabet
    (${h.link(request, sources['ipa2005'])}) and on ${h.link(request, sources['hayes2009'])}.
    This is accomplished by creating a mapping relationship from each IPA segment to a set
    of features (Moran 2012). In this way, the IPA is a pivot for interoperability across
    all resources in PHOIBLE because their contents are encoded in Unicode IPA.
</p>

<p>For a detailed description of PHOIBLE, see
    ${h.link(request, sources['moran2012a'])}
    ${h.external_link("https://digital.lib.washington.edu/researchworks/handle/1773/22452", label=" ")}.
    For examples of some of the research we are doing with PHOIBLE, see:

    ${h.link(request, sources['moranetal2012'])},
    ${h.link(request, sources['cysouwetal2012'])},
    ${h.link(request, sources['mccloyetal2013'])}
    and Moran &amp; Blasi, Cross-linguistic comparison of complexity measures in phonological systems, forthcoming.
</p>

<p>
    PHOIBLE was funded in 2009 by a grant from the Royalty Research Fund at the University of Washington.
</p>
##    moran2012b ##<li>Moran, Steven. 2012b. Using Linked Data to Create a Typological Knowledge Base. In Linked Data in Linguistics: Representing and Connecting Language Data and Language Metadata, Christian Chiarcos, Sebastian Nordhoff and Sebastian Hellmann (eds). Springer, Heidelberg.</li>
