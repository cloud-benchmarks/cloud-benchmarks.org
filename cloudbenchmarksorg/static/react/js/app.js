var React = require('react');
var Table = require('./components/Table.react');

function renderTable(data) {
  React.render(
    <Table data={data}/>,
    document.getElementById('submissions')
  );
}

window.renderTable = renderTable;
