import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface DetectedField {
  original_column: string;
  suggested_field: string;
  data_type: string;
  confidence: number;
  keywords: string[];
}

export interface AnalysisResult {
  detected_fields: DetectedField[];
  statistics: {
    total_files: number;
    total_columns: number;
    unique_columns: number;
  };
  column_frequency: { [key: string]: number };
}

@Injectable({
  providedIn: 'root'
})
export class AutodetectService {
  private apiUrl = 'http://localhost:5000/api/autodetect';

  constructor(private http: HttpClient) {}

  analyzeFiles(files: FileList): Observable<AnalysisResult> {
    const formData = new FormData();
    
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }
    
    return this.http.post<AnalysisResult>(`${this.apiUrl}/analyze`, formData);
  }

  createProfileFromDetection(
    detectedFields: DetectedField[],
    profileName: string,
    profileDescription: string = ''
  ): Observable<any> {
    return this.http.post(`${this.apiUrl}/create-profile`, {
      detected_fields: detectedFields,
      profile_name: profileName,
      profile_description: profileDescription
    });
  }
}
