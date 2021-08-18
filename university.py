class Admission:

    def __init__(self):
        self.num_of_students_to_accept = int(input())
        self.departments = {"Biotech": [], "Chemistry": [], "Engineering": [], "Mathematics": [], "Physics": []}
        self.applicants = self.sort_applicants_by_gpa()

    @staticmethod
    def sort_applicants_by_gpa():
        """Sorts Students by their GPA and stores them in self.applicants (list)"""
        with open('applicants.txt', 'r') as file:
            applicants = [line.replace("\n", "").split() for line in file]
        applicants.sort(key=lambda x: (-float(x[2]), x[0] + x[1]))
        return applicants

    def select_applicants(self):
        """Increments i (Department1, Department2, Department3)"""
        for i in range(3, 6):
            self.select_applicants_by_department(i)

    def select_applicants_by_department(self, priority):
        remaining_applicants = self.applicants
        for applicant in self.applicants[:]:
            for department in self.departments.keys():
                if applicant[priority] == department and len(self.departments.get(department)) < self.num_of_students_to_accept:
                    self.departments[department].append(applicant)
                    remaining_applicants.remove(applicant)
        self.applicants = remaining_applicants

    def display_selected_applicants(self):
        for key in self.departments.keys():
            self.departments[key].sort(key=lambda x: (-float(x[2]), x[0] + x[1]))
            print(key)
            for student in self.departments[key]:
                print(" ".join(student[0:3]))
            print("")


uni = Admission()
uni.select_applicants()
uni.display_selected_applicants()
