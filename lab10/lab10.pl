% ==========================================
% ЛАБОРАТОРНАЯ РАБОТА 10: SWI-PROLOG
% ==========================================

% --- Базовые факты: студенты и курсы ---
student(aida).
student(miras).
student(dana).
student(timur).
student(aliya). % Добавлено по Заданию 1

course(programming_1).
course(programming_2).
course(data_structures).
course(databases).
course(artificial_intelligence).
course(machine_learning).

% completed(Student, Course) - освоенные курсы
completed(aida, programming_1).
completed(aida, programming_2).
completed(aida, data_structures).
completed(aida, databases).

completed(miras, programming_1).
completed(miras, databases).

completed(dana, programming_1).
completed(dana, programming_2).
completed(dana, data_structures).

completed(timur, programming_1).

% Добавлено по Заданию 1 для студента aliya
completed(aliya, programming_1).
completed(aliya, programming_2).

% requires(Course, Prerequisite) - непосредственные пререквизиты
requires(programming_2, programming_1).
requires(data_structures, programming_2).
requires(artificial_intelligence, data_structures).
requires(artificial_intelligence, databases).
requires(machine_learning, artificial_intelligence).


% --- Задание 2: Правила и составные цели ---
ai_candidate(Student) :-
    completed(Student, data_structures),
    completed(Student, databases).

% Сильный студент: освоил programming_2 и data_structures
strong_student(Student) :-
    student(Student),
    completed(Student, programming_2),
    completed(Student, data_structures).


% --- Задание 4: Проверка непосредственного допуска ---
missing_direct(Student, Course, Prerequisite) :-
    student(Student),
    requires(Course, Prerequisite),
    \+ completed(Student, Prerequisite).

immediate_eligible(Student, Course) :-
    student(Student),
    course(Course),
    \+ missing_direct(Student, Course, _).


% --- Задание 5: Транзитивные пререквизиты (рекурсия) ---
prerequisite(Course, Prerequisite) :-
    requires(Course, Prerequisite).
prerequisite(Course, Prerequisite) :-
    requires(Course, Intermediate),
    prerequisite(Intermediate, Prerequisite).


% --- Задание 6: Полный допуск и список недостающих курсов ---
missing_all(Student, Course, Missing) :-
    setof(P,
          (prerequisite(Course, P), \+ completed(Student, P)),
          Missing), !.
missing_all(_Student, _Course, []).

eligible(Student, Course) :-
    student(Student),
    course(Course),
    missing_all(Student, Course, []).


% --- Задание 7: Безопасность рекурсии (защита от циклов) ---
safe_prerequisite(Course, Prerequisite) :-
    safe_prerequisite(Course, Prerequisite, [Course]).

safe_prerequisite(Course, Prerequisite, _) :-
    requires(Course, Prerequisite).

safe_prerequisite(Course, Prerequisite, Visited) :-
    requires(Course, Next),
    \+ memberchk(Next, Visited),
    safe_prerequisite(Next, Prerequisite, [Next|Visited]).


% --- Задание 8: Интегрированный отчёт ---
recommendation(Student, Course, eligible, []) :-
    eligible(Student, Course).
recommendation(Student, Course, missing, Missing) :-
    missing_all(Student, Course, Missing),
    Missing \= [].


% ==========================================
% ИНДИВИДУАЛЬНЫЙ ВАРИАНТ №2: Запись на курс (can_enroll/2)
% ==========================================
% Факты о вместимости курсов (лимит мест)
course_capacity(artificial_intelligence, 2).
course_capacity(machine_learning, 1).
course_capacity(databases, 5).

% Текущее количество записанных студентов на курс
enrolled_count(artificial_intelligence, 1).
enrolled_count(machine_learning, 1).
enrolled_count(databases, 2).

% Правило: студент может записаться на курс, если он имеет полный допуск (eligible) 
% и на курсе есть свободные места (capacity > current).
can_enroll(Student, Course) :-
    eligible(Student, Course),
    course_capacity(Course, Capacity),
    enrolled_count(Course, Current),
    Current < Capacity.