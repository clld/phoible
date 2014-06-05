<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>
##<% squib = ctx.files.get('%s-squib.pdf' % ctx.id) %>

<h2>${_('Contribution')} ${ctx.name}</h2>

##% if squib:
##<div class="tabbable">
##    <ul class="nav nav-tabs">
##        <li class="active"><a href="#segments" data-toggle="tab">Segments</a></li>
##        <li><a href="#source" data-toggle="tab">Source</a></li>
##    </ul>
##    <div class="tab-content" style="overflow: visible;">
##        <div id="segments" class="tab-pane active">
##            ${request.get_datatable('values', h.models.Value, contribution=ctx).render()}
##        </div>
##        <div id="source" class="tab-pane">
##            <object data="${request.file_url(ctx.files['%s-squib.pdf' % ctx.id])}" type="application/pdf" style="width: 100%;" height="800">
##                alt : <a href="${request.file_url(ctx.files['%s-squib.pdf' % ctx.id])}">squib</a>
##            </object>
##        </div>
##    </div>
##</div>
##% else:
    % if ctx.source_url:
        ${h.external_link(ctx.source_url, label=ctx.source)}
    % endif
    ${request.get_datatable('values', h.models.Value, contribution=ctx).render()}
##% endif

<%def name="sidebar()">
    <%util:well title="Contributor">
        ${h.linked_contributors(request, ctx)}
        ${h.cite_button(request, ctx)}
        ${util.stacked_links(ref.source for ref in ctx.primary_contributors[0].references)}
    </%util:well>
    <%util:well title="Sources">
        ${util.stacked_links(ref.source for ref in ctx.references)}
    </%util:well>
    <%util:well>
        <h3>${h.link(request, ctx.language)}</h3>
        ${util.language_meta(lang=ctx.language)}
    </%util:well>
</%def>
