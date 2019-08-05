import { Component, OnInit } from '@angular/core';
import {Bitch} from '../../models/bitch'
import {BitchService} from "../../bitch.service";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  bitchez: Bitch[] = [];

  constructor(private bitchService: BitchService) { }

  ngOnInit() {
    this.getBitchez();
  }

  getBitchez() {
    this.bitchService.getBitchez()
        .subscribe(bitchez => this.bitchez = bitchez.slice(1,5));
  }

}
