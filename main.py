# coding=utf-8
# 分析:
# 这个问题因为总收入和总工资都是固定的，总毛利也一定固定
# 所以没有最优解，不能算背包问题
# 也许有多个解，这里只输出最先得到的解
# 思路:
# 用DFS来进行搜索：如果有员工只有一家公司能去，那他就没有选择
# 同时用贪心来减少搜索量：同等条件下首先分配薪水高的员工
# 优化：
# 在计算的中间针对情形数据需要throw exception，这里没有处理
# 还有很多地方可以剪枝，来减少时间和空间，嘛，你也不一定用python，改成java的时候自己剪好了w

from copy import deepcopy

employee_salary = {'a': 26, 'b': 30, 'c': 40}
project_benefit_list = {'A': 100, 'B': 200}
project_limitation_list = {'A': [0.1, 0.5], 'B': [0.2, 0.4]}
employee_project_mapper = {'a': ['A', 'B'], 'b': ['A'], 'c': ['B']}

# init project_salary_interval
project_salary_interval = {}
for project in project_benefit_list.keys():
    benefit = project_benefit_list[project]
    lower = project_limitation_list[project][0] * benefit
    higher = project_limitation_list[project][1] * benefit
    project_salary_interval[project] = [lower, higher]

print("the salary interval for every project are :")
for item in project_salary_interval.items():
    print item[0], item[1]
print

# judge data
lower_sum = 0
higher_sum = 0
for key, value in project_salary_interval.items():
    lower = value[0]
    higher = value[1]
    lower_sum += lower
    higher_sum += higher
    lower_flag = False
    higher_flag = False
    if lower > sum(employee_salary.values()):
        print("gross profit of project " + key + " is too big or too small")
        print("stop cause there is no answer")
        exit(1)
    for salary in employee_salary.values():
        if lower <= salary:
            lower_flag = True
        if higher >= salary:
            higher_flag = True
        if lower_flag and higher_flag:
            break
    if not (lower_flag and higher_flag):
        print("gross profit of project " + key + " is too big or too small")
        print("stop cause there is no answer")
        exit(1)
if lower_sum > sum(employee_salary.values()) or higher_sum < sum(employee_salary.values()):
    print("stop cause there is no answer")
    exit(1)


def main():
    # init current_project_salary
    current_project_salary = {}
    for project in project_salary_interval.keys():
        current_project_salary[project] = 0
    print "current_project_salary: "
    print current_project_salary

    # init current_employee_project_mapper
    current_employee_project_mapper = update_current_employee_project_mapper(employee_project_mapper,
                                                                             current_project_salary)
    print "current_employee_project_mapper: "
    print current_employee_project_mapper

    # init remain_employee
    current_remain_employee = {}
    for employee, salary in employee_salary.items():
        current_remain_employee[employee] = [salary, len(current_employee_project_mapper[employee])]
    current_remain_employee = sorted(current_remain_employee.items(), key=lambda item: item[1][1])
    print "current_remain_employee"
    print current_remain_employee
    print

    current = {'A': [], 'B': []}
    ans = loop (current_remain_employee, current_project_salary, current_employee_project_mapper, current)

    print "one available answer is: "
    print ans


def loop(current_remain_employee, current_project_salary, current_employee_project_mapper, current):
    if len(current_remain_employee) <= 0:
        return current
    for item in current_remain_employee:
        employee = item[0]
        for project in current_employee_project_mapper[employee]:
            next_project_salary = dict(current_project_salary)
            next_project_salary[project] += employee_salary[employee]
            next_remain_employee = list(current_remain_employee)
            next_remain_employee.remove(item)
            next_employee_project_mapper = dict(current_employee_project_mapper)
            next_employee_project_mapper.pop(employee)
            next_employee_project_mapper = update_current_employee_project_mapper(next_employee_project_mapper,
                                                                                  next_project_salary)
            next = dict(current)
            next[project].append(employee)
            return loop(next_remain_employee, next_project_salary, next_employee_project_mapper, next)


def update_current_employee_project_mapper(current_employee_project_mapper, current_project_salary):
    next_employee_project_mapper = dict(current_employee_project_mapper)
    for employee, projects in current_employee_project_mapper.items():
        for p in projects:
            if employee_salary[employee] + current_project_salary[p] > project_salary_interval[p][1]:
                next_employee_project_mapper[employee].remove(p)
    return next_employee_project_mapper


main()
