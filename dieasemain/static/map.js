let latitude;
let longitude;
let locationOk = false;

const x = document.getElementById("location");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
        locationOk = true
        return;
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    latitude = position.coords.latitude;
    longitude = position.coords.longitude;
    x.innerHTML = "Latitude: " + position.coords.latitude +
        "<br>Longitude: " + position.coords.longitude;
}

// // 위치정보 사용
// function getLocation() {
// 	if (navigator.geolocation) {
// 		navigator.geolocation.getCurrentPosition(getAddressByCoords,redirectLocation, geo_options);
//         //navigator.geolocation.getCurrentPosition(successCallback,errorCallback,{ timeout: 10_000 });
// 	} else {
// 		location.href = "/mbl/test/selectAddressList.do";
// 	}
// }

// //성공했을 때
// function getAddressByCoords(position) {
// 	var longitude = position.coords.longitude;
// 	var latitude = position.coords.latitude;
// 	console.log(longitude);
//     console.log(latitude);
//     //★★위도 경도 정보를 가지고 서버 사이드로 넘어가는 부분
// 	location.href = "/mbl/test/selectAddressList.do?longitude=" + longitude + "&latitude=" + latitude;
// }

// //에러났을 때
// function redirectLocation(error) {
// 	location.href = "/mbl/error/selectAddressList.do";
// }

// //타임아웃
// var geo_options = {
// 	maximumAge        : 5000, 
// 	timeout           : 3000
// };

