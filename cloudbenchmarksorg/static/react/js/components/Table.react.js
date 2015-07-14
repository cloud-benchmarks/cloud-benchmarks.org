var React = require('react');
var BS = require('react-bootstrap');
var _ = require('underscore');
var cx = require('classnames');

var util = require('../util.js')

const SORT_DESC = -1;
const SORT_ASC = 1;
const SORT_NONE = 0;


var Table = React.createClass({

  getInitialState: function() {
    return {
      sortCol: 'Date',
      sortDir: SORT_DESC,
      sortFunc: (a) => a.created_at || ''
    }
  },

  _getSortDir: function(col) {
    if (this.state.sortCol === col) {
      return this.state.sortDir;
    }
    return SORT_NONE;
  },

  _handleSort: function(col, dir, func) {
    this.setState({
      sortCol: col,
      sortDir: dir,
      sortFunc: func
    });
  },

  _makeColumnHeader: function(name, sortFunc) {
    return (
      <ColumnHeader
        name={name}
        sortDir={this._getSortDir(name)}
        sortFunc={sortFunc}
        onSort={this._handleSort}
      />
    );
  },

  _formatCloud: function(env) {
    if (env.region) {
      return (
        <a href={`/environments/${env.provider_type}`}>{env.region}</a>
      );
    }
    return (
      <a href={`/environments/${env.name}`}>{env.name}</a>
    );
  },

  _formatServices: function(sub) {
    return (
      <ul className="services">
        {_.map(sub.services, (charm) => {
          return (
            <li>
              <a href={`/services/${charm.charm_name}`}>{charm.charm_name} ({charm.unit_count})</a>
            </li>
          );
        })}
      </ul>
    );
  },

  render: function() {
    var p = this.props;
    var sortedData = _.sortBy(p.data, this.state.sortFunc);

    if (this.state.sortDir === SORT_DESC) {
      sortedData = sortedData.reverse();
    }

    var rows = sortedData
      .map(function (s) {
        return (
          <tr key={s.id}>
            <td>{this._formatCloud(s.environment)}</td>
            <td>{s.benchmark_name}</td>
            <td>{this._formatServices(s)}</td>
            <td>
              <a href={`/submissions/${s.id}`}>{util.formatResult(s.result)}</a>
            </td>
            <td>
              <a href={`/submissions/${s.id}`} title={s.created_at}>{util.timeDeltaHtml(s.created_at)}</a>
            </td>
            <td>{s.rank}</td>
          </tr>
        );
    }.bind(this));

    return (
      <table className="table">
        <thead>
          <tr>
            {this._makeColumnHeader('Cloud', (a) => a.environment.name)}
            {this._makeColumnHeader('Benchmark', (a) => a.benchmark_name)}
            {this._makeColumnHeader('Workload', (a) => Object.keys(a.services).join(' '))}
            {this._makeColumnHeader('Result', (a) => a._result_value)}
            {this._makeColumnHeader('Date', (a) => a.created_at)}
            {this._makeColumnHeader('Rank', (a) => a.rank)}
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    );
  }
});

var ColumnHeader = React.createClass({
  propTypes: {
    name: React.PropTypes.string,
    sortable: React.PropTypes.bool,
    sortDir: React.PropTypes.number,
    sortFunc: React.PropTypes.func,
    onSort: React.PropTypes.func
  },

  getDefaultProps: function() {
    return {
      name: null,
      sortable: true,
      sortDir: SORT_NONE,
      sortFunc: undefined
    }
  },

  _handleClick: function() {
    if (!this.props.sortable) {
      return;
    }

    var sortDir = this.props.sortDir === SORT_NONE ?
      SORT_DESC :
      -this.props.sortDir;
    this.props.onSort(this.props.name, sortDir, this.props.sortFunc);
  },

  render: function() {
    return (
      <th
        onClick={this._handleClick}
        className={cx(this.props.sortable ? 'sortable' : false)}
      >
        {this.props.name || this.props.children}
        {this.props.sortDir === SORT_DESC &&
            <BS.Glyphicon glyph='triangle-bottom' />}
        {this.props.sortDir === SORT_ASC &&
            <BS.Glyphicon glyph='triangle-top' />}
      </th>
    );
  }
});

module.exports = Table;
