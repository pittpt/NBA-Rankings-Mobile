import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomePage } from './home.page';

const routes: Routes = [
  {
    path: '',
    component: HomePage
    // children: [
    //   {
    //     path: 'fav',
    //     children: [
    //       {
    //         path:'',
    //         loadChildren: './fav/fav.module#FavPageRoutingModule'
    //       }
    //     ]
    //   },
    //   {
    //     path: 'ranking',
    //     children: [
    //       {
    //         path:'',
    //         loadChildren: './ranking/ranking.module#RankingPageRoutingModule'
    //       }
    //     ]
    //   },
    //   {
    //     path:'',
    //     redirectTo: '/home/fav',
    //     pathMatch: 'full'
    //   }
    // ]
  }
  // {
  //   path:'',
  //   redirectTo: '/home/fav',
  //   pathMatch: 'full'
  // }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HomePageRoutingModule {}
