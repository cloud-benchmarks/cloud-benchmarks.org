<%def name="service_list(submission)">
  <ul class="services">
  %for c in submission.services().values():
    <li><a href="/services/${c.charm_name}">${c.charm_name} (${c.unit_count})</a></li>
  %endfor
  </ul>
</%def>

<%def name="format_result(result)">
  %if isinstance(result, dict) and 'value' in result:
    ${result['value']} ${result.get('units', '')}
  %else:
    ${result}
  %endif
</%def>

<%def name="environment_link(env)">
  %if env.region:
    <a href="/environments/${env.provider_type}">${env.provider_type}</a>:<a href="/environments/${env.name}">${env.region}</a>
  %else:
    <a href="/environments/${env.name}">${env.name}</a>
  %endif
</%def>

<%def name="submissions_table(data)">
<div id="submissions">
  <span class="glyphicon glyphicon-refresh spinning"></span>
</div>
<script>
  window.onload = function() {
    renderTable(${data | n});
  };
</script>
</%def>

<%def name="keyval_table(pairs, headers=None, caption=None)">
<% headers = headers or ('Key', 'Value') %>
<table class="table">
  %if caption:
    <caption>${caption}</caption>
  %endif
  <thead>
    <tr>
      %for h in headers or ('Key', 'Value'):
      <th>${h}</th>
      %endfor
    </tr>
  </thead>
  <tbody>
  %for key, val in pairs:
    <tr>
      <td>${key}</td>
      <td>${format_result(val)}</td>
    </tr>
  %endfor
  </tbody>
</table>
</%def>
