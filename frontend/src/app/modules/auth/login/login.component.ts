import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators, AbstractControl } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  form: FormGroup;
  error = '';
  loading = false;

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });

    if (this.route.snapshot.queryParamMap.get('sessionExpired')) {
      this.error = 'Session expired. Please log in again.';
    }
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.error = '';

    const { email, password } = this.form.value;
    this.auth.login(email, password).subscribe({
      next: (res) => {
        const role = res.data.user.role;
        if (role === 'ADMIN') this.router.navigate(['/admin/dashboard']);
        else if (role === 'DOCTOR') this.router.navigate(['/doctor/dashboard']);
        else this.router.navigate(['/patient/dashboard']);
      },
      error: (err) => {
        this.error = err.error?.message
          || (err.status === 0 ? 'Cannot connect to the server. Please try again.' : `Login failed (${err.status})`);
        this.loading = false;
      },
      complete: () => (this.loading = false)
    });
  }
}
