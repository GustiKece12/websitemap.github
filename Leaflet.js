// Setelah routingControl dibuat
routingControl.on('routesfound', function(e) {
    var routes = e.routes;
    var summary = routes[0].summary;

    var estimatedDistance = summary.totalDistance / 1000; // dalam km
    var estimatedTime = summary.totalTime / 60; // dalam menit

    document.getElementById('output').innerHTML = `
      Estimasi Jarak: ${estimatedDistance.toFixed(2)} km <br>
      Estimasi Waktu: ${estimatedTime.toFixed(0)} menit
    `;
});
