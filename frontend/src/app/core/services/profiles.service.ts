import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Profile {
  id?: string;
  nombre: string;
  descripcion: string;
  campos: Field[];
  fecha_creacion?: string;
  fecha_actualizacion?: string;
}

export interface Field {
  nombre: string;
  palabras_clave: string[];
  tipo_dato: string;
  requerido: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class ProfilesService {
  private apiUrl = 'http://localhost:5000/api/profiles';

  constructor(private http: HttpClient) {}

  getAllProfiles(): Observable<Profile[]> {
    return this.http.get<Profile[]>(this.apiUrl);
  }

  getProfile(id: string): Observable<Profile> {
    return this.http.get<Profile>(`${this.apiUrl}/${id}`);
  }

  createProfile(profile: Profile): Observable<Profile> {
    return this.http.post<Profile>(this.apiUrl, profile);
  }

  updateProfile(id: string, profile: Profile): Observable<Profile> {
    return this.http.put<Profile>(`${this.apiUrl}/${id}`, profile);
  }

  deleteProfile(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  searchProfiles(query: string): Observable<Profile[]> {
    return this.http.get<Profile[]>(`${this.apiUrl}/search?q=${query}`);
  }
}
