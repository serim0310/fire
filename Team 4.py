import pandas as pd

def classify_flammability(material):
    # 물질별 인화점 정보 (물질: 인화점)
    flash_points = {
        "휘발유": -43,
        "아세톤": -20,
        "이황화탄소": -30,
        "등유": 38,
        "니트로벤젠": 88,
        "에탄올": 13,
        "메탄올": 11,
        "톨루엔": 4,
        "헥산": -22,
        "벤젠": -11
    }

    # 인화점에 따른 가연성 점수를 결정합니다
    if material in flash_points:
        flash_point = flash_points[material]
        if flash_point >= 60:
            return 1  # 낮은 가연성
        elif 30 <= flash_point < 60:
            return 2
        elif 0 <= flash_point < 30:
            return 3
        elif -20 <= flash_point < 0:
            return 4
        elif flash_point < -20:
            return 5  # 높은 가연성
    else:
        return "알 수 없는 물질입니다."  # 물질 정보가 없을 때


def calculate_fire_risk(ignition_sources, fire_load, temperature, humidity, flammability):
    """
    화재 위험 점수를 계산합니다.
    ignition_sources: 점화원 수 (1-5)
    fire_load: 화재 하중 (1-5)
    temperature: 온도 (°C)
    humidity: 습도 (%)
    flammability: 가연성 (1-5)
    """
    # 온도와 습도의 영향을 고려하여 점수를 계산합니다
    temperature_factor = temperature / 30  # 온도의 영향을 30°C로 스케일링
    humidity_factor = (100 - humidity) / 50  # 습도가 낮을수록 위험 증가
    weather_factor = temperature_factor * humidity_factor

    return flammability * ignition_sources * fire_load * weather_factor  # 최종 화재 위험 점수


def get_fire_risk_level(score):
    """
    화재 위험 점수에 따른 등급을 반환합니다.
    score: 화재 위험 점수
    반환값: 위험도 등급 (문자열)
    """
    # 점수에 따라 위험도를 결정합니다
    if score <= 20:
        return "매우 낮음 (Very Low)"
    elif score <= 40:
        return "낮음 (Low)"
    elif score <= 60:
        return "보통 (Moderate)"
    elif score <= 80:
        return "높음 (High)"
    else:
        return "매우 높음 (Very High)"


def get_input(prompt, value_type=int):
    """
    사용자 입력을 받아 특정 타입의 값을 반환합니다.
    올바른 값이 입력될 때까지 반복합니다.
    """
    # 사용자로부터 입력을 받아 올바른 타입으로 변환합니다
    while True:
        try:
            value = value_type(input(prompt))
            return value
        except ValueError:
            print("올바른 값을 입력해주세요.")


def get_ranged_input(prompt, min_value, max_value):
    """
    사용자 입력을 받아 특정 범위 내의 정수를 반환합니다.
    """
    # 범위 내의 값을 입력받도록 합니다
    while True:
        value = get_input(prompt)
        if min_value <= value <= max_value:
            return value
        else:
            print(f"값은 {min_value}에서 {max_value} 사이여야 합니다. 다시 입력해주세요.")


def main():
    results = []  # 결과를 저장할 리스트

    while True:
        # 프로그램 시작 메시지
        print("\n화재 위험 평가 프로그램입니다.")

        # 물질 이름 입력 받기
        material_name = input(
            "[물질 보기] 휘발유, 아세톤, 이황화탄소, 등유, 니트로벤젠, 에탄올, 메탄올, 톨루엔, 헥산, 벤젠\n물질 이름을 입력하세요 (종료하려면 '종료' 입력): ")

        if material_name == "종료":
            print("프로그램을 종료합니다.")
            break

        # 가연성 점수 계산
        flammability = classify_flammability(material_name)

        if isinstance(flammability, str):
            print(flammability)
            continue

        # 사용자로부터 점화원 수, 화재 하중, 온도, 습도 입력받기
        ignition_sources = get_ranged_input("점화원 수 (1-5): ", 1, 5)
        fire_load = get_ranged_input("화재 하중 (1-5): ", 1, 5)
        temperature = get_input("온도 (°C): ", float)
        humidity = get_ranged_input("습도 (%): ", 0, 100)

        # 화재 위험 점수 계산
        fire_risk_score = calculate_fire_risk(ignition_sources, fire_load, temperature, humidity, flammability)
        fire_risk_level = get_fire_risk_level(fire_risk_score)

        # 결과 저장
        result = {
            "물질": material_name,
            "가연성": flammability,
            "점화원 수": ignition_sources,
            "화재 하중": fire_load,
            "온도": temperature,
            "습도": humidity,
            "화재 위험 점수": fire_risk_score,
            "화재 위험 등급": fire_risk_level
        }
        results.append(result)

        # 결과 출력
        print(f"{material_name}의 인화점 분류 점수는: {flammability}점입니다.")
        print(f"화재 위험 점수: {fire_risk_score:.2f}")
        print(f"화재 위험 등급: {fire_risk_level}")

    # DataFrame으로 변환하여 엑셀 파일로 저장
    if results:
        df = pd.DataFrame(results)
        df.to_excel("fire_risk_assessment.xlsx", index=False)
        print("결과가 fire_risk_assessment.xlsx 파일에 저장되었습니다.")

# 유닛 테스트 함수
def test_calculate_fire_risk():
    # 테스트 케이스를 통해 함수 검증
    assert calculate_fire_risk(1, 1, 20, 50, 1) == 0.4
    assert calculate_fire_risk(5, 5, 30, 0, 5) == 125.0
    assert calculate_fire_risk(3, 3, 25, 20, 3) == 16.8
    print("모든 테스트 통과")

if __name__ == "__main__":
    main()
    test_calculate_fire_risk()