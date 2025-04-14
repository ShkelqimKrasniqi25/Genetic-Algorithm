import tkinter as tk
from tkinter import ttk
import random
from job_shop_problem import JobShopProblem
from genetic_algorithm import GeneticAlgorithm

class JobShopGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Job-Shop Scheduling me Algoritmin Gjenetik")

        # Definimi i etiketave për secilën fushë hyrëse të përdoruesit
        labels = ["Numri i puneve:", "Numri i makinerive:", "Madhësia e popullates:",
                  "Numri i brezave:", "Norma e mutacionit (0-1):"]
        self.entries = []
        
        # Krijimi i etiketave dhe fushave për hyrje
        for i, label in enumerate(labels):
            ttk.Label(root, text=label).grid(row=i, column=0, sticky="w")  # Vendos etiketa në kolonën 0
            entry = ttk.Entry(root)  # Krijo një fushë për hyrje
            entry.grid(row=i, column=1)  # Vendos fushën e hyrjes në kolonën 1
            self.entries.append(entry)  # Shto fushën në listën e hyrjeve për përdorim të mëtejshëm

        # Vlerat e paracaktuara për fushat e hyrjes
        self.entries[0].insert(0, "3")     # numri i punëve
        self.entries[1].insert(0, "3")     # numri i makinave
        self.entries[2].insert(0, "20")    # madhësia e popullatës
        self.entries[3].insert(0, "50")    # numri i brezave
        self.entries[4].insert(0, "0.1")   # norma e mutacionit

        # Krijimi i një butoni që nis ekzekutimin e algoritmit kur shtypet
        self.run_button = ttk.Button(root, text="Nis Algoritmin", command=self.run_algorithm)
        self.run_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Krijimi i një dritareje për shfaqjen e rezultateve të algoritmit
        self.result_text = tk.Text(root, height=20, width=70)
        self.result_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def generate_random_jobs(self, num_jobs, num_machines):
        # Krijon të dhëna të rastësishme për punët dhe operacionet e tyre
        jobs_data = []
        for _ in range(num_jobs):
            # Për secilën punë, krijo një listë të makinave të rastësishme
            machines = random.sample(range(num_machines), num_machines)
            # Krijo operacione me kohëzgjatje të rastësishme për çdo makinë
            job = [(m, random.randint(1, 5)) for m in machines]
            jobs_data.append(job)
        return jobs_data

    def run_algorithm(self):
        # Kjo metodë ekzekuton algoritmin gjenetik për të gjetur një zgjidhje të mundshme
        try:
            # Merr vlerat e vendosura nga përdoruesi dhe i konverton në numra
            num_jobs = int(self.entries[0].get())
            num_machines = int(self.entries[1].get())
            population_size = int(self.entries[2].get())
            generations = int(self.entries[3].get())
            mutation_rate = float(self.entries[4].get())
        except ValueError:
            # Nëse ndodhin gabime me formatin e vlerave të hyrjes, shfaq një mesazh gabimi
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "⚠️ Ju lutem vendosni vlera te sakta numerike!")
            return

        # Krijon punë dhe operacione të rastësishme për problemin
        jobs_data = self.generate_random_jobs(num_jobs, num_machines)
        # Krijon një objekt problemi për Job-Shop
        problem = JobShopProblem(jobs_data)
        # Krijon dhe ekzekuton algoritmin gjenetik për këtë problem
        ga = GeneticAlgorithm(problem, population_size, generations, mutation_rate)
        best, makespan = ga.run()  # Kallzon rezultatet e algoritmit: kromozomi më i mirë dhe koha më e shkurtër

        # Fshinë dhe paraqiten rezultatet në GUI
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"🔧 Lista e puneve (Jobs):\n\n")

        # Shfaq secilën punë dhe operacionet e saj
        for i, job in enumerate(jobs_data):
            self.result_text.insert(tk.END, f"📌 Job {i+1}:\n")
            for m_id, dur in job:
                self.result_text.insert(tk.END, f"   ➤ Makina M{m_id} për {dur} njësi kohe, p.sh Minuta:\n")
            self.result_text.insert(tk.END, "\n")

        # Shfaq kohën më të shkurtër totale për përfundimin e të gjitha punëve
        self.result_text.insert(tk.END, f"✅ Koha më e shkurtër totale për te përfunduar te gjitha punët: {makespan}\n")

        # Krijimi i emrave për punët dhe formatimi i kromozomit për shfaqje
        job_names = [f"Job {i+1}" for i in range(num_jobs)]  # Krijo emra për punët
        formatted_chromosome = " → ".join([job_names[best[i]] for i in range(len(best))])  # Formato kromozomin

        # Shfaq kromozomin më të mirë të mundshëm
        self.result_text.insert(tk.END, f"🧬 Kromozomi më i mire/puna më e mirë: {formatted_chromosome}\n")

# Nisja e aplikacionit GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = JobShopGUI(root)
    root.mainloop()
