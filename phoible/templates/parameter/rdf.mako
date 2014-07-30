<%inherit file="../resource_rdf.mako"/>
<%block name="properties">
    <% cls = ctx.segment_class.capitalize() if ctx.segment_class else None %>
    <rdf:type rdf:resource="${str(h.rdf.NAMESPACES['gold'][cls if cls in ['Consonant', 'Vowel'] else 'Segment'])}"/>
    % if cls:
    <dcterms:description>${cls}</dcterms:description>
    % endif
    % for d in ctx.data:
    <gold:feature rdf:parseType="Resource">
        <rdf:type rdf:resource="${str(h.rdf.NAMESPACES['gold']['PhoneticProperty'])}"/>
        <rdfs:label xml:lang="en">${d.key}</rdfs:label>
        <skos:prefLabel xml:lang="en">${d.key}</skos:prefLabel>
        <dcterms:title xml:lang="en">${d.key}</dcterms:title>
        <dcterms:description>${d.value}</dcterms:description>
    </gold:feature>
    % endfor
    % for vs in ctx.valuesets:
    <dcterms:isReferencedBy rdf:resource="${request.resource_url(vs)}"/>
    % endfor
    % if ctx.jsondatadict.get('wikipedia_url'):
    <rdfs:seeAlso rdf:resource="${ctx.jsondatadict['wikipedia_url'].replace('en.wikipedia.org/wiki', 'dbpedia.org/resource')}"/>
    % endif
</%block>
