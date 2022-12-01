am5.ready(function () {
  graficas_clustered.forEach((grafica) => {
    // Create root element
    // https://www.amcharts.com/docs/v5/getting-started/#Root_element
    var root = am5.Root.new(grafica[0]);

    // Set themes
    // https://www.amcharts.com/docs/v5/concepts/themes/
    root.setThemes([am5themes_Animated.new(root)]);

    // Create chart
    // https://www.amcharts.com/docs/v5/charts/xy-chart/
    var chart = root.container.children.push(
      am5xy.XYChart.new(root, {
        panX: false,
        panY: false,
        layout: root.verticalLayout,
      })
    );

    // Add legend
    // https://www.amcharts.com/docs/v5/charts/xy-chart/legend-xy-series/
    var legend = chart.children.push(
      am5.Legend.new(root, {
        centerX: am5.p50,
        x: am5.p50,
      })
    );

    // Data
    var data = grafica[1]["datos"];

    // Create axes
    // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/

    var yAxis = chart.yAxes.push(
      am5xy.CategoryAxis.new(root, {
        categoryField: "categoria",
        renderer: am5xy.AxisRendererY.new(root, {
          inversed: true,
          cellStartLocation: 0.1,
          cellEndLocation: 0.9,
        }),
      })
    );

    yAxis.data.setAll(data);

    var xAxis = chart.xAxes.push(
      am5xy.ValueAxis.new(root, {
        renderer: am5xy.AxisRendererX.new(root, {}),
        min: 1,
        extraMax: 0.11,
      })
    );

    // Add series
    // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
    function createSeries(field, name) {
      var series = chart.series.push(
        am5xy.ColumnSeries.new(root, {
          name: name,
          xAxis: xAxis,
          yAxis: yAxis,
          valueXField: field,
          categoryYField: "categoria",
          sequencedInterpolation: true,
          tooltip: am5.Tooltip.new(root, {
            pointerOrientation: "horizontal",
            oversizedBehavior: "wrap",
            labelText: "{categoryY}: {valueX}",
          }),
        })
      );

      series.columns.template.setAll({
        height: am5.p100,
      });

      series.bullets.push(function () {
        return am5.Bullet.new(root, {
          locationX: 0.97,
          locationY: 0.5,
          sprite: am5.Label.new(root, {
            centerY: am5.p50,
            text: "{valueX}",
            populateText: true,
          }),
        });
      });

      series.data.setAll(data);
      series.appear();

      return series;
    }

    grafica[2].forEach((element) => {
      var series = createSeries(element, element);

      series.events.on("datavalidated", function (ev) {
        var series = ev.target;
        if (ev.target.data.length < 1) {
          // Generate placeholder data
          var categoryField = series.get("categoryField");
          var valueField = series.get("valueField");
          var placeholder = [];
          for (i = 0; i < 3; i++) {
            var item = {};
            item[categoryField] = "";
            item[valueField] = 1;
            placeholder.push(item);
          }
          series.data.setAll(placeholder);

          // Disable ticks/labels
          // series.labels.template.set("forceHidden", true);
          // series.ticks.template.set("forceHidden", true);

          // Show modal
          modal.open();
        } else {
          // Re-enable ticks/labels
          // series.labels.template.set("forceHidden", false);
          // series.ticks.template.set("forceHidden", false);

          // Hide modal
          modal.close();
        }
      });
    });

    // Create modal for a "no data" note
    var modal = am5.Modal.new(root, {
      content: "La gráfica no tiene datos.",
    });

    // Add legend
    // https://www.amcharts.com/docs/v5/charts/xy-chart/legend-xy-series/
    var legend = chart.children.push(
      am5.Legend.new(root, {
        centerX: am5.p50,
        x: am5.p50,
      })
    );

    legend.data.setAll(chart.series.values);

    // Add cursor
    // https://www.amcharts.com/docs/v5/charts/xy-chart/cursor/
    var cursor = chart.set(
      "cursor",
      am5xy.XYCursor.new(root, {
        behavior: "zoomY",
      })
    );

    yAxis.get("renderer").labels.template.setAll({
      oversizedBehavior: "wrap",
      maxWidth: 115,
    });

    cursor.lineY.set("forceHidden", true);
    cursor.lineX.set("forceHidden", true);

    // Make stuff animate on load
    // https://www.amcharts.com/docs/v5/concepts/animations/
    chart.appear(1000, 100);
  }); // end am5.ready()
});
