import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.css']
})
export class SearchBarComponent implements OnInit {

  constructor(private http: HttpClient) { }

  searchTerm: string = '';
  ngOnInit(): void {
  }

  sendSearchTerm(): void {
    this.http.post('http://localhost:5000/download?url=', { searchTerm: this.searchTerm }).subscribe((data) => {
      console.log(data);
    });
  }

}
