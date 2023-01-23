import { Component, OnInit } from '@angular/core';
import { DataProviderService } from '../data-provider.service';

@Component({
  selector: 'app-ranking',
  templateUrl: './ranking.page.html',
  styleUrls: ['./ranking.page.scss'],
})
export class RankingPage implements OnInit {
  ranks = [];
  range = 1;
  flask = 'http://d4c6-34-122-82-131.ngrok.io';

  constructor(private myProvider: DataProviderService) { }

  ngOnInit() {
  }

  ionViewDidEnter(){
    this.myProvider.getRankings(1,this.ranks,this.flask,null);
  }

  loadData(event){
    this.range+=10;
    this.myProvider.getRankings(this.range,this.ranks,this.flask,event);
  }


}
