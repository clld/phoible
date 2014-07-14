<%inherit file="app.mako"/>

<%block name="brand">
    <a class="brand" href="${request.route_url('dataset')}" title="${request.dataset.name}">[ˈfɔɪ.bl̴]</a>
</%block>

${next.body()}
