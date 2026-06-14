import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { debounceTime, distinctUntilChanged } from 'rxjs';
import { PatientApiService } from '../../../services/patient.service';
import { Doctor } from '../../../models';

@Component({
  selector: 'app-book-appointment',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './book-appointment.component.html',
  styleUrl: './book-appointment.component.css'
})
export class BookAppointmentComponent implements OnInit {
  form: FormGroup;
  searchForm: FormGroup;
  doctors: Doctor[] = [];
  availableSlots: string[] = [];
  occupiedSlots: string[] = [];
  message = '';
  error = '';
  loading = false;
  searching = false;
  minDate = new Date().toISOString().slice(0, 10);

  constructor(private fb: FormBuilder, private patientApi: PatientApiService) {
    this.searchForm = this.fb.group({
      search: [''],
      speciality: ['']
    });
    this.form = this.fb.group({
      doctor_id: ['', Validators.required],
      appointment_date: ['', Validators.required],
      appointment_time: ['', Validators.required],
      symptoms: [''],
      visit_type: ['In-Person', Validators.required]
    });
  }

  ngOnInit(): void {
    this.loadDoctors();
    this.searchForm.valueChanges
      .pipe(debounceTime(300), distinctUntilChanged())
      .subscribe(() => this.loadDoctors());
    this.form.get('doctor_id')?.valueChanges.subscribe(() => this.loadAvailability());
    this.form.get('appointment_date')?.valueChanges.subscribe(() => this.loadAvailability());
  }

  loadDoctors(): void {
    const { search, speciality } = this.searchForm.value;
    this.searching = true;
    this.error = '';
    this.patientApi.getDoctors(search, speciality).subscribe({
      next: (res) => {
        if (res.success) this.doctors = res.data;
        this.form.patchValue({ doctor_id: '', appointment_time: '' }, { emitEvent: false });
        this.availableSlots = [];
        this.occupiedSlots = [];
      },
      error: (err) => {
        this.error = err.error?.message || 'Doctor search failed';
        this.searching = false;
      },
      complete: () => (this.searching = false)
    });
  }

  loadAvailability(): void {
    this.availableSlots = [];
    this.occupiedSlots = [];
    this.form.patchValue({ appointment_time: '' }, { emitEvent: false });
    const doctorId = +this.form.value.doctor_id;
    const date = this.form.value.appointment_date;
    if (!doctorId || !date) return;

    this.patientApi.getDoctorAvailability(doctorId, date).subscribe({
      next: (res) => {
        this.availableSlots = res.data.available_slots;
        this.occupiedSlots = res.data.occupied_slots;
      },
      error: (err) => (this.error = err.error?.message || 'Availability lookup failed')
    });
  }

  chooseSlot(slot: string): void {
    this.form.patchValue({ appointment_time: slot });
  }

  isSelectedSlotAvailable(): boolean {
    return this.availableSlots.includes(this.form.value.appointment_time);
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.error = '';
    this.message = '';

    const { doctor_id, appointment_date, appointment_time, symptoms, visit_type } = this.form.value;
    const dateTime = `${appointment_date}T${appointment_time}:00`;

    this.patientApi.bookAppointment({
      doctor_id: +doctor_id,
      appointment_date: dateTime,
      symptoms,
      visit_type
    }).subscribe({
      next: (res) => {
        this.message = res.message;
        this.form.reset({ visit_type: 'In-Person' });
        this.availableSlots = [];
        this.occupiedSlots = [];
        this.loadDoctors();
      },
      error: (err) => {
        this.error = err.error?.message || 'Booking failed';
        this.loading = false;
      },
      complete: () => (this.loading = false)
    });
  }
}
