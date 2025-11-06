import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { ProfilesService, Profile } from '../../core/services/profiles.service';

@Component({
  selector: 'app-profiles',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './profiles.component.html',
  styleUrls: ['./profiles.component.scss']
})
export class ProfilesComponent implements OnInit {
  profiles: Profile[] = [];
  selectedProfile: Profile | null = null;
  showCreateForm = false;
  loading = false;
  error: string | null = null;

  newProfile: Profile = {
    nombre: '',
    descripcion: '',
    campos: []
  };

  constructor(private profilesService: ProfilesService) {}

  ngOnInit(): void {
    this.loadProfiles();
  }

  loadProfiles(): void {
    this.loading = true;
    this.profilesService.getAllProfiles().subscribe({
      next: (profiles) => {
        this.profiles = profiles;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar perfiles: ' + err.message;
        this.loading = false;
      }
    });
  }

  createProfile(): void {
    if (!this.newProfile.nombre) {
      this.error = 'El nombre es requerido';
      return;
    }

    this.loading = true;
    this.profilesService.createProfile(this.newProfile).subscribe({
      next: () => {
        this.showCreateForm = false;
        this.loadProfiles();
        this.resetForm();
      },
      error: (err) => {
        this.error = 'Error al crear perfil: ' + err.message;
        this.loading = false;
      }
    });
  }

  deleteProfile(id: string): void {
    if (!confirm('¿Estás seguro de eliminar este perfil?')) {
      return;
    }

    this.profilesService.deleteProfile(id).subscribe({
      next: () => {
        this.loadProfiles();
      },
      error: (err) => {
        this.error = 'Error al eliminar perfil: ' + err.message;
      }
    });
  }

  resetForm(): void {
    this.newProfile = {
      nombre: '',
      descripcion: '',
      campos: []
    };
    this.error = null;
  }
}
