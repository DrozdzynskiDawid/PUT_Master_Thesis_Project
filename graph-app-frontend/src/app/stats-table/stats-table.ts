import { Component, inject, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { DataService } from '../service/data.service';
import { API_ENDPOINTS } from '../service/api-endpoints';
import { forkJoin } from 'rxjs';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'stats-table',
  standalone: true,
  imports: [MatButtonModule, MatTableModule, CommonModule],
  templateUrl: './stats-table.html',
  styleUrl: './stats-table.scss',
})
export class StatsTable {
  private dataService = inject(DataService);
  displayedColumns: string[] = ['type', 'nodes', 'edges', 'density', 'avgDegree', 'connected'];
  
  errorMessage = signal<string | null>(null);
  dataSource = signal<any[]>([]);

  fetchData() {
    this.errorMessage.set(null);

    forkJoin({
      main: this.dataService.sendPostRequestJson<any>(API_ENDPOINTS.STATS, this.dataService.graphLLMJsonData()),
      clique: this.dataService.sendPostRequestJson<any>(API_ENDPOINTS.STATS, this.dataService.graphCliqueJsonData()),
      selected: this.dataService.sendPostRequestJson<any>(API_ENDPOINTS.STATS, this.dataService.graphSelectedCliqueJsonData())
    }).subscribe({
      next: (results) => {
        this.dataSource.set([
          this.mapToRow('Podstawowy', results.main),
          this.mapToRow('Clique', results.clique),
          this.mapToRow('Selected Clique', results.selected)
        ]);
      },
      error: (err) => {
        console.error('Error:', err);
        this.errorMessage.set('Error occurred while fetching statistics data.');
      }
    });
  }

  private mapToRow(typeName: string, data: any) {
    return {
      type: typeName,
      nodes: data.nodes_count,
      edges: data.edges_count,
      density: data.density?.toFixed(4),
      avgDegree: data.average_degree?.toFixed(2),
      connected: data.is_connected ? 'Tak' : 'Nie'
    };
  }
}