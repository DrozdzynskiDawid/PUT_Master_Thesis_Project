import { HttpClient } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { DataService } from '../service/data.service';

@Component({
  selector: 'text-from-dataset',
  standalone: true,
  imports: [CommonModule, MatButtonModule],
  templateUrl: './text-from-dataset.html',
  styleUrl: './text-from-dataset.scss',
})
export class TextFromDataset {
  private http = inject(HttpClient);
  private dataService = inject(DataService);
  text = signal<string | null>(null);
  isLoading = signal<boolean>(false);
  errorMessage = signal<string | null>(null);

  getText() {
      this.isLoading.set(true);
      this.errorMessage.set(null);
      this.text.set(null);
      
      const apiUrl = 'http://localhost:8000/api/random-text';

      this.http.get<{text: string}>(apiUrl).subscribe({
        next: (response) => {
          this.text.set(response.text);
          this.dataService.textFromDataset.set(response.text);
          this.isLoading.set(false);
        },
        error: (err) => {
          console.error('Błąd:', err);
          this.errorMessage.set('Wystąpił błąd podczas pobierania.');
          this.isLoading.set(false);
        }
      });
    }
}
