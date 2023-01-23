import { Component, OnInit } from '@angular/core';
import { DataProviderService } from '../data-provider.service';

@Component({
  selector: 'app-fav',
  templateUrl: './fav.page.html',
  styleUrls: ['./fav.page.scss'],
})


export class FavPage implements OnInit {
  favPlayers = [];
  box = [];
  flask = 'http://d4c6-34-122-82-131.ngrok.io';

  constructor(private myProvider: DataProviderService) {}

  

  ionViewDidEnter() {
    
    console.log('Start ionViewDidEnter');
    this.myProvider.getFavorites(this.favPlayers,this.flask);
    console.log(this.favPlayers)
  }

  clearFav(){
    this.myProvider.clearFavorites(this.box,this.flask);
    console.log(this.box)
  }

  ngOnInit() {
  }

}
