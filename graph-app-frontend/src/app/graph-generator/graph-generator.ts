import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { DataService } from '../service/data.service';
import { API_ENDPOINTS } from '../service/api-endpoints';

@Component({
  selector: 'graph-generator',
  standalone: true,
  imports: [CommonModule, MatButtonModule],
  templateUrl: './graph-generator.html',
  styleUrl: './graph-generator.scss',
})
export class GraphGenerator {
  private dataService = inject(DataService);
  isLoading = signal<boolean>(false);
  errorMessage = signal<string | null>(null);
  graphImageUrl = signal<string | null>(null);
  hypergraphImageUrl = signal<string | null>(null);
  givenText = this.dataService.textFromDataset;

  fetchData() {
    this.isLoading.set(true);
    this.errorMessage.set(null);
    if (this.graphImageUrl()) {
      URL.revokeObjectURL(this.graphImageUrl()!);
      this.graphImageUrl.set(null);
    }
    if (this.hypergraphImageUrl()) {
      URL.revokeObjectURL(this.hypergraphImageUrl()!);
      this.hypergraphImageUrl.set(null);
    }

    this.dataService.sendPostRequestJson<any>(`${API_ENDPOINTS.GRAPH}`, {text: this.givenText()}).subscribe({
      next: (response) => {
        this.generateGraphImageFromData(response);
        this.dataService.graphLLMJsonData.set(response);
        console.log('JSON graph data:', response);
      },
      error: (err) => {
        console.error('Error:', err);
        this.errorMessage.set('Error occurred while fetching graph data.');
        this.isLoading.set(false);
      }
    });

    this.dataService.sendPostRequestJson<any>(`${API_ENDPOINTS.HYPERGRAPH}`, {text: this.givenText()}).subscribe({
      next: (response) => {
        this.generateHypergraphImageFromData(response);
        console.log('JSON hypergraph data:', response);
        this.dataService.hypergraphJsonData.set(response);
      },
      error: (err) => {
        console.error('Error:', err);
        this.errorMessage.set('Error occurred while fetching hypergraph data.');
        this.isLoading.set(false);
      }
    });
  }

  private generateGraphImageFromData(graphData: any) {
    this.dataService.sendPostRequestBlob(`${API_ENDPOINTS.GRAPH_PNG}`, graphData).subscribe({
      next: (imageBlob: Blob) => {
        const url = URL.createObjectURL(imageBlob);
        this.graphImageUrl.set(url);
        this.isLoading.set(false); 
      },
      error: (err) => {
        console.error('Error generating image:', err);
        this.errorMessage.set('An error occurred while generating the graph image from JSON data.');
        this.isLoading.set(false);
      }
    });
  }

  private generateHypergraphImageFromData(hypergraphData: any) {
    this.dataService.sendPostRequestBlob(`${API_ENDPOINTS.HYPERGRAPH_PNG}`, hypergraphData).subscribe({
      next: (imageBlob: Blob) => {
        const url = URL.createObjectURL(imageBlob);
        this.hypergraphImageUrl.set(url);
        this.isLoading.set(false); 
      },
      error: (err) => {
        console.error('Error generating image:', err);
        this.errorMessage.set('An error occurred while generating the hypergraph image from JSON data.');
        this.isLoading.set(false);
      }
    });
  }
}
