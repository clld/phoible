<%inherit file="app.mako"/>

<%block name="header">
    <a href="${request.route_url('dataset')}">
        <img style="margin: 10px 0 10px 20px;" height="71" width="250" src="${request.static_url('phoible:static/phoible.png')}"/>
    </a>
</%block>

${next.body()}
