import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { DataProviderService } from '../data-provider.service';
import { Data } from '../../../src/Models/model';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  public data$: Observable<Data>;
  tyr =[];
  itemListData = []
  playerName: String;
  errorMes: String;
  searchTerm: String;
  players = [];
  added = true;
  flask = 'http://d4c6-34-122-82-131.ngrok.io';


  constructor(private myProvider: DataProviderService) {}

  ionViewDidEnter() {
    console.log('Start ionViewDidEnter');
    this.myProvider.getPlayer(this.players,this.flask);
  }

  setPlayer(){
    this.itemListData = []
    this.added = true;
    this.playerName = this.searchTerm
    this.myProvider.getData(this.playerName,this.itemListData,this.flask);
  }

  addFav(){
    this.tyr = [];
    this.added = false;
    this.myProvider.addFavorites(this.playerName,this.flask,this.tyr);
    console.log(this.tyr)
  }

}
