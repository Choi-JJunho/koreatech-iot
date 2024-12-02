import math

NX = 149  # X축 격자점 수
NY = 253  # Y축 격자점 수

class LamcParameter:
    def __init__(self):
        self.Re = 6371.00877  # 지구 반경(km)
        self.grid = 5.0  # 격자 간격(km)
        self.slat1 = 30.0  # 표준위도 1
        self.slat2 = 60.0  # 표준위도 2
        self.olon = 126.0  # 기준점 경도
        self.olat = 38.0  # 기준점 위도
        self.xo = 210 / self.grid  # 기준점 X좌표
        self.yo = 675 / self.grid  # 기준점 Y좌표
        self.first = 0

def lamcproj(lon, lat, x, y, code, map_params):
    PI = math.asin(1.0) * 2.0
    DEGRAD = PI / 180.0
    RADDEG = 180.0 / PI

    if map_params.first == 0:
        re = map_params.Re / map_params.grid
        slat1 = map_params.slat1 * DEGRAD
        slat2 = map_params.slat2 * DEGRAD
        olon = map_params.olon * DEGRAD
        olat = map_params.olat * DEGRAD

        sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
        sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
        sf = math.tan(PI * 0.25 + slat1 * 0.5)
        sf = math.pow(sf, sn) * math.cos(slat1) / sn
        ro = math.tan(PI * 0.25 + olat * 0.5)
        ro = re * sf / math.pow(ro, sn)
        map_params.first = 1
    else:
        re = map_params.Re / map_params.grid
        slat1 = map_params.slat1 * DEGRAD
        slat2 = map_params.slat2 * DEGRAD
        olon = map_params.olon * DEGRAD
        olat = map_params.olat * DEGRAD

        sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
        sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
        sf = math.tan(PI * 0.25 + slat1 * 0.5)
        sf = math.pow(sf, sn) * math.cos(slat1) / sn
        ro = math.tan(PI * 0.25 + olat * 0.5)
        ro = re * sf / math.pow(ro, sn)

    if code == 0:  # (lon,lat) -> (x,y)
        ra = math.tan(PI * 0.25 + float(lat) * DEGRAD * 0.5)
        ra = re * sf / math.pow(ra, sn)
        theta = float(lon) * DEGRAD - olon
        if theta > PI:
            theta -= 2.0 * PI
        if theta < -PI:
            theta += 2.0 * PI
        theta *= sn
        x[0] = ra * math.sin(theta) + map_params.xo
        y[0] = ro - ra * math.cos(theta) + map_params.yo
    else:  # (x,y) -> (lon,lat)
        xn = float(x[0]) - map_params.xo
        yn = ro - float(y[0]) + map_params.yo
        ra = math.sqrt(xn * xn + yn * yn)
        if sn < 0.0:
            ra = -ra
        alat = math.pow((re * sf / ra), (1.0 / sn))
        alat = 2.0 * math.atan(alat) - PI * 0.5
        if abs(xn) <= 0.0:
            theta = 0.0
        else:
            if abs(yn) <= 0.0:
                theta = PI * 0.5
                if xn < 0.0:
                    theta = -theta
            else:
                theta = math.atan2(xn, yn)
        alon = theta / sn + olon
        lat[0] = alat * RADDEG
        lon[0] = alon * RADDEG

    return 0

def map_conv(lon, lat, x, y, code, map_params):
    if code == 0:  # 위경도 -> 격자
        lamcproj(float(lon), float(lat), x, y, 0, map_params)
        x[0] = int(x[0] + 1.5)
        y[0] = int(y[0] + 1.5)
    else:  # 격자 -> 위경도
        x1 = float(x[0]) - 1
        y1 = float(y[0]) - 1
        lamcproj(lon, lat, [x1], [y1], 1, map_params)
        lon[0] = float(lon[0])
        lat[0] = float(lat[0])
    return 0

def convert_coords(code, a, b):
    """
    좌표 변환 함수
    code: 0(위경도->격자) 또는 1(격자->위경도)
    a: 경도(code=0) 또는 X격자(code=1)
    b: 위도(code=0) 또는 Y격자(code=1)
    returns: (nx, ny) or (lon, lat)
    """
    map_params = LamcParameter()

    if code == 1:
        if float(a) < 1 or float(a) > NX or float(b) < 1 or float(b) > NY:
            raise ValueError(f"X-grid range [1,{NX}] / Y-grid range [1,{NY}]")
        x = [float(a)]
        y = [float(b)]
        lon = [0.0]
        lat = [0.0]
        map_conv(lon, lat, x, y, 1, map_params)
        return int(x[0]), int(y[0])
    elif code == 0:
        x = [0.0]
        y = [0.0]
        map_conv(float(a), float(b), x, y, 0, map_params)
        return int(x[0]), int(y[0])
    else:
        raise ValueError("Code must be 0 or 1")

# # 사용 예시
# if __name__ == "__main__":
#     # 위경도 -> 격자 변환
#     nx, ny = convert_coords(0, 127.302637, 36.766497)
#     print(f"nx={nx}, ny={ny}")
#
#     # 격자 -> 위경도 변환
#     lon, lat = convert_coords(1, 55, 127)
#     print(f"lon={lon}, lat={lat}")
