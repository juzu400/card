class UniversityAdmission:
    applicants = []
    accepted = {'Biotech': [], 'Chemistry': [], 'Engineering': [], 'Mathematics': [], 'Physics': []}
    used = []
    score_id = 1
    sec_score_id = 0

    def __init__(self, number, departments):
        self.number = number
        self.departments = departments

    def map_dep_score(self, dep):
        if dep == 'Biotech':
            self.score_id = 2
            self.sec_score_id = 1
        elif dep == 'Chemistry':
            self.score_id = 2
            self.sec_score_id = 0
        elif dep == 'Engineering':
            self.score_id = 4
            self.sec_score_id = 3
        elif dep == 'Mathematics':
            self.score_id = 3
            self.sec_score_id = 0
        elif dep == 'Physics':
            self.score_id = 1
            self.sec_score_id = 3

    def get_applicants(self):
        """get applicants from file
        update self.applicants: [[full name, score, physics result, chemistry result, math result, computer science result], [full name, ...], ...]"""

        with open('applicants.txt', 'r') as open_file:
            for line in open_file:
                first_name, last_name, p_score, ch_score, m_score, cs_score, uni_score, first_prio, sec_prio, third_prio = line.split()
                self.applicants.append([first_name + ' ' + last_name, float(p_score), float(ch_score), float(m_score), float(cs_score), float(uni_score), first_prio, sec_prio, third_prio])

    def sort(self):
        if self.sec_score_id == 0:
            self.applicants = sorted(self.applicants, key=lambda x: (-max(x[self.score_id], x[5]), x[0]))
        else:
            self.applicants = sorted(self.applicants, key=lambda x: (-max(((x[self.score_id] + x[self.sec_score_id]) / 2), x[5]), x[0]))

    def accept(self, round_, dep):
        """update self.accepted {Biotech: [(full_name, score), (full_name, score), ...], Chemistry: [..], ...}
           accepted persons are sorted by score and full name """
        right_prio = [applicant for applicant in self.applicants if applicant[round_] == dep]
        for applicant in right_prio:
            if self.sec_score_id == 0:
                name = applicant[0]
                if applicant[5] > applicant[self.score_id]:
                    score = applicant[5]
                else:
                    score = applicant[self.score_id]
            else:
                name = applicant[0]
                if applicant[5] > (applicant[self.score_id] + applicant[self.sec_score_id]) / 2:
                    score = applicant[5]
                else:
                    score = (applicant[self.score_id] + applicant[self.sec_score_id]) / 2
            if len(self.accepted[dep]) < self.number and name not in self.used:
                self.accepted[dep].append((name, score))
                self.used.append(name)
        self.accepted[dep] = sorted(self.accepted[dep], key=lambda x: (-x[1], x[0]))

    def output(self):
        for dep in self.departments:
            if dep == 'Biotech':
                with open('biotech.txt', 'w') as f1:
                    for name, score in self.accepted[dep]:
                        f1.write(name + ' ' + str(score) + '\n')

            if dep == 'Chemistry':
                with open('chemistry.txt', 'w') as f2:
                    for name, score in self.accepted[dep]:
                        f2.write(name + ' ' + str(score) + '\n')

            if dep == 'Engineering':
                with open('engineering.txt', 'w') as f3:
                    for name, score in self.accepted[dep]:
                        f3.write(name + ' ' + str(score) + '\n')

            if dep == 'Mathematics':
                with open('mathematics.txt', 'w') as f4:
                    for name, score in self.accepted[dep]:
                        f4.write(name + ' ' + str(score) + '\n')

            if dep == 'Physics':
                with open('physics.txt', 'w') as f5:
                    for name, score in self.accepted[dep]:
                        f5.write(name + ' ' + str(score) + '\n')


task = UniversityAdmission(int(input()), ['Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics'])
task.get_applicants()
for i in range(6, 9):
    for department in task.departments:
        task.map_dep_score(department)
        task.sort()
        task.accept(i, department)

task.output()
