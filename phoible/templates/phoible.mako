<%inherit file="app.mako"/>

##<%block name="header">
##    <a href="${request.route_url('dataset')}">
##        <img style="margin-left: 2em;" width="100" height="100" src="${request.static_url('phoible:static/phoible.png')}"/>
##    </a>
##</%block>

${next.body()}
