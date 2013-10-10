<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<h2>${_('Contribution')} ${ctx.name}</h2>

${util.data()}

<% dt = request.registry.queryUtility(h.interfaces.IDataTable, 'values'); dt = dt(request, h.models.Value, contribution=ctx) %>
<div>
    ${dt.render()}
</div>

<%def name="sidebar()">
    <%util:well>
        <h3>${h.link(request, ctx.language)}</h3>
        ${util.language_meta(lang=ctx.language)}
    </%util:well>
</%def>
