<%inherit file="../base.mako"/>
<%namespace name="lib" file="../lib.mako"/>

${submission.svg | n}
<pre>${submission.bundle_yaml}</pre>
${lib.keyval_table(submission.summary.items(), caption='Summary')}
${lib.keyval_table(submission.results.items(), caption='Results')}
${lib.keyval_table(submission.parameters.items(), caption='Parameters')}
