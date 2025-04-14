class JobShopProblem:
    def __init__(self, jobs_data):
        # Konstruktori i klasës JobShopProblem, merr të dhënat e punëve
        self.jobs_data = jobs_data  # Të dhënat e punëve dhe operacionet e tyre (listë e listave, ku secila listë përfaqëson operacionet e një pune)
        self.num_jobs = len(jobs_data)  # Numri i punëve (numri i elementeve në jobs_data)
        # Kjo përcakton numrin maksimal të makinave duke marrë makinat nga të gjitha punët dhe operacionet
        self.num_machines = max(machine for job in jobs_data for machine, _ in job) + 1

    def decode(self, chromosome):
        # Metoda decode interpreton kromozomin dhe llogarit kohën totale për zgjidhjen
        job_counters = [0] * self.num_jobs  # Një listë për të numëruar sa operacione janë kryer për secilën punë
        machine_times = [0] * self.num_machines  # Një listë për ruajtjen e kohës së fundit për çdo makinë
        job_times = [0] * self.num_jobs  # Një listë për ruajtjen e kohës së fundit për çdo punë

        # Përshtat kromozomin përmes të gjitha punëve të caktuara
        for job_id in chromosome:
            # Gjejmë numrin e operacionit për secilën punë
            op_index = job_counters[job_id]
            if op_index >= len(self.jobs_data[job_id]):
                continue  # Nëse kemi përfunduar të gjitha operacionet për këtë punë, kalojmë në punën tjetër

            # Merr informacionin për makinën dhe kohëzgjatjen e operacionit
            machine_id, duration = self.jobs_data[job_id][op_index]
            # Përcakto kohën e fillimit për këtë operacion, që është maksimale mes kohës së fundit të makinerisë dhe kohës së fundit të punës
            start_time = max(machine_times[machine_id], job_times[job_id])
            end_time = start_time + duration  # Koha e përfundimit të operacionit

            # Përdor këto informacione për të përditësuar kohët e makinës dhe punës
            machine_times[machine_id] = end_time  # Përditëso koha e fundit për këtë makinë
            job_times[job_id] = end_time  # Përditëso koha e fundit për këtë punë
            job_counters[job_id] += 1  # Rrit numrin e operacioneve të kryera për këtë punë

        # Kthejmë kohën maksimale të përfundimit të punëve, që tregon kohën totale të zbatimit të të gjitha punëve
        return max(job_times)
