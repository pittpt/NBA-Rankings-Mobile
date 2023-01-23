import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Data } from '../../src/Models/model';


@Injectable({
  providedIn: 'root'
})
export class DataProviderService {

  constructor(private http:HttpClient) {
    console.log('Create Data Provider');
  }

  getData(name,itemList,url){
    this.http.get(url+'/getplayerstats?name='+name).subscribe(data=>
      {
        for(let i=0;i<8;i++){
          console.log(data[i]);
          itemList.push(data[i]);
        }
      }
    );
   }

  getPlayer(players,url){
    this.http.get(url+'/listplayer?year=2019').subscribe(data=>
      {
        for(let i=0;i<data['data'].length;i++){
          // console.log(data['data'][i]);
          players.push(data['data'][i]);
        }
      }
    );
  }

  addFavorites(name,url,tyr){
    return this.http.get(url+'/insertfav?name='+name).subscribe(data=>
      {
        for(let i=0;i<8;i++){
          console.log(data[i]);
          tyr.push(data[i]);
        }
      }
    );
  }

  getFavorites(favplayers,url){
    this.http.get(url+'/fetchfav').subscribe(data=>
      {
        for(let i=0;i<data['data'].length;i++){
          console.log(data['data'][i]);
          favplayers.push(data['data'][i]);
        }
      }
    );
  }

  clearFavorites(box,url){
    this.http.get(url+'/favremove').subscribe(data=>
      {
        for(let i=0;i<1;i++){
          console.log(data[i]);
          box.push(data[i]);
        }
      }
    );
  }

  getRankings(range,rank,url,event){
    this.http.get(url+'/getranks?range='+range).subscribe(data=>
      {
        for(let i=0;i<data['data'].length;i++){
          console.log(data['data'][i]);
          rank.push(data['data'][i]);
        }
      }
    );
    if(range!=0){
      event.target.complete();
    }
    
  }

}
