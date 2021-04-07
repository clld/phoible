<%inherit file="home_comp.mako"/>

<%block name="head">
    <link href="${request.static_url('clld:web/static/css/charissil.css')}" rel="stylesheet">
</%block>

${content|n}

