${ctx.primary_contributors[0].description}${'' if ctx.primary_contributors[0].description.endswith('.') else '.'} ${request.dataset.published.year if request.dataset.published else ctx.updated.year}. ${ctx.language.name} sound inventory (${ctx.primary_contributors[0].id}).
In: ${request.dataset.formatted_editors()|n} (eds.)
${request.dataset.description}.
${request.dataset.publisher_place}: ${request.dataset.publisher_name}.
(Available online at http://${request.dataset.domain}${request.resource_path(ctx)}, Accessed on ${h.datetime.date.today()}.)
