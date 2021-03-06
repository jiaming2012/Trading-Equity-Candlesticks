$(function() {
	$('#container').highcharts({
		data: {		
			table: 'datatable'
		},
		chart: {
			type: 'column'
		},
		title: {
			text: 'This works'
		},
		yAxis: {
			allowDecimals: false,
			title: {
				text: 'Unis'
			}
		},
		tooltip: {
			formatter: function() {
				return '<b>' + this.series.name + '</b><br/>' +
					this.point.y + ' ' + this.point.name.toLowerCase();
			}
		}
	});
});
