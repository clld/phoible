<%inherit file="app.mako"/>

<%block name="brand">
    <a class="brand" style="padding-top: 7px; padding-bottom: 5px;" href="${request.route_url('dataset')}" title="${request.dataset.name}">
        ##[ˈfɔɪ.bl̴]
        <img height="25" src="${request.static_url('phoible:static/phoible_icon.png')}"/>
    </a>
</%block>

${next.body()}
