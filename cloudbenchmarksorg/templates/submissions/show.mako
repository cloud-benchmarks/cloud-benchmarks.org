<%! import random %>

<%inherit file="../base.mako"/>
<%namespace name="lib" file="../lib.mako"/>

${submission.svg | n}
<pre>${submission.bundle_yaml}</pre>
${lib.keyval_table(submission.summary.items(), caption='Summary')}
${lib.keyval_table(submission.results.items(), caption='Results')}
${lib.keyval_table(submission.parameters.items(), caption='Parameters')}


%if related_submissions:
<h2>Related Results</h2>
<table class="table">
  <tbody>

  <%
    max_width = float(max(s._result_value for s in related_submissions + [submission]))
  %>

  %for s in [submission] + related_submissions:
    <%
      width = (s._result_value / max_width) * 500
      r, g, b, a = random.randint(0, 0xFF), random.randint(0, 0xFF), random.randint(0, 0xFF), .35
    %>
    <tr>
      <td>${'this ({})'.format(s.environment.name) if s == submission else s.environment.name}</td>
      <td>
        <a class="bar" href="/submissions/${s.id}">
          <div style="width:${width}px; background-color:rgba(${r},${g},${b},${a})">
            <p>${s._result_value} ${submission.result.get('units', '')}</p>
          </div>
        </a>
      </td>
    </tr>
  %endfor
  </tbody>
</table>
%endif
