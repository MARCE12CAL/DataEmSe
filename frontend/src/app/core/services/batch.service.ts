import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface BatchConfig {
  profile_name: string;
  csv_path: string;
  output_folder: string;
  file_prefix?: string;
}

export interface BatchScriptResponse {
  script: string;
  filename: string;
}

@Injectable({
  providedIn: 'root'
})
export class BatchService {
  private apiUrl = 'http://localhost:5000/api/batch';

  constructor(private http: HttpClient) {}

  generateScript(config: BatchConfig): Observable<BatchScriptResponse> {
    return this.http.post<BatchScriptResponse>(`${this.apiUrl}/generate-script`, config);
  }

  downloadScript(script: string, filename: string): void {
    const blob = new Blob([script], { type: 'text/x-python' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(url);
  }

  saveJob(jobName: string, config: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/save-job`, {
      job_name: jobName,
      config: config
    });
  }

  getJob(jobName: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/get-job/${jobName}`);
  }
}
