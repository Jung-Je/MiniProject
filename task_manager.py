import json
import os

#작업을 저장할 파일 경로
TASK_FILE = '07_todo/tasks.json'

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r', encoding ='utf-8') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, 'w', encoding ='utf-8') as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def view_tasks():
    pass

def complete_task(task_number):
    pass

def delete_task(task_number):
    pass

def add_task(task_name):
    tasks = load_tasks()
    task = {'mame': task_name, 'completed': False}
    tasks.append(task)
    save_tasks(tasks)
    print(f"'{task_name} 작업이 추가 되었습니다.")

def show_menu():
    print("작업 관리 애플리케이션")
    print("1. 할 일 추가")
    print("2. 할 일 목록 보기")
    print("3. 할 일 완료")
    print("4. 할 일 삭제")
    print("5. 종료")
    print()

def main():
    while True:
        show_menu()
        choice = input("원하는 작업을 선택하세요 (1~5): ")

        if choice == '1':
            task_name = input("추가할 작업을 입력하세요") #수업 끝나고 맛잇는거 먹을래요
            add_task(task_name) #함수를 호출 또는 실행한다고 함 -> 함수이름(매개변수)
        elif choice == '2':
            view_tasks()
        elif choice == '3':    
            task_number = int(input("완료할 작업 번호를 입력하세요: "))
            complete_task(task_number)
        elif choice == '4':  
            task_number = int(input("삭제할 작업 번호를 입력하세요: "))
            delete_task(task_number)
        elif choice == '5':
            print("프로그램 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 1번부터 5번까지 기능 중 하나를 선택해주세요")    


if __name__ == '__main__':
    main()