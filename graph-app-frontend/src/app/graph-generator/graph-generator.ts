import { Component, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'graph-generator',
  standalone: true,
  imports: [CommonModule, MatButtonModule],
  templateUrl: './graph-generator.html',
  styleUrl: './graph-generator.scss',
})
export class GraphGenerator {
  private http = inject(HttpClient);
  jsonData = signal<any | null>(null);
  isLoading = signal<boolean>(false);
  errorMessage = signal<string | null>(null);
  imageUrl = signal<string | null>(null);

  fetchData() {
    this.isLoading.set(true);
    this.errorMessage.set(null);
    this.jsonData.set(null);
    if (this.imageUrl()) {
      URL.revokeObjectURL(this.imageUrl()!);
      this.imageUrl.set(null);
    }
    
    const apiUrl = 'http://localhost:8000/api/graph';

    this.http.get<any>(apiUrl).subscribe({
      next: (response) => {
        this.jsonData.set(response);
        this.generateImageFromData(response);
      },
      error: (err) => {
        console.error('Błąd:', err);
        this.errorMessage.set('Wystąpił błąd podczas pobierania.');
        this.isLoading.set(false);
      }
    });
  }

  private generateImageFromData(graphData: any) {
    const imageApiUrl = 'http://localhost:8000/api/graph/visualization';

    this.http.post(imageApiUrl, graphData, { responseType: 'blob' }).subscribe({
      next: (imageBlob: Blob) => {
        const url = URL.createObjectURL(imageBlob);
        this.imageUrl.set(url);
        this.isLoading.set(false); 
      },
      error: (err) => {
        console.error('Błąd generowania obrazka:', err);
        this.errorMessage.set('Wystąpił błąd podczas generowania obrazka na podstawie JSON-a.');
        this.isLoading.set(false);
      }
    });
  }
}
