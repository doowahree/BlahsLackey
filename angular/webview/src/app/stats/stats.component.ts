import {Component, Input, OnInit} from '@angular/core';
import * as d3 from 'd3';
import * as wordleDb from '../../proto/WordlDb';
import {CredentialsProviderService} from "../credentials-provider.service";
import {HttpClient} from "@angular/common/http";
import {Tabulator as TabulatorNamespace, TabulatorFull as Tabulator} from 'tabulator-tables';


interface ProtoDataResponse {
  data: string;
}

interface TableRowData {
  gameId: string;
  attempts: number;
  maxAttempts: number;
  avg: number;
  fails: number;
}

interface AverageData {
  data: {
    [key: string]: {
      game_id: string,
      total: number,
      fails: number,
      counts: number
    }
  }
}

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})
export class StatsComponent implements OnInit {
  private svg?: d3.Selection<SVGGElement, unknown, HTMLElement, any>;
  private svgCanvas?: d3.Selection<SVGGElement, unknown, HTMLElement, any>;
  private statsTable?: Tabulator;
  private margin = 50;
  private width = 500 - (this.margin * 2);
  private height = 250 - (this.margin * 2);
  private currentSeason?: wordleDb.WordleSeason;
  private static readonly numberExtractor = /\d+/;

  private readonly encoder: TextEncoder = new TextEncoder();


  _selectedUser: string = '';
  get selectedUser(): string {
    return this._selectedUser;
  }

  @Input('selectedUser')
  set selectedUser(val: string) {
    this._selectedUser = val;
    this.drawSeason(this._selectedUser);
  }

  availableUsers: Array<{ display: string, id: string }> = [];
  season: string = '';

  constructor(private readonly credentials: CredentialsProviderService, private readonly http: HttpClient) {
  }

  ngOnInit(): void {
    this.statsTable = new Tabulator('#statsTable', {
      height: 400,
      layout: "fitColumns",
      data: [],
      columns: [
        {title: "Game Id", field: "gameId", width: 150, sorter: this.sortGameId},
        {title: "Attempt", field: "attempts", hozAlign: "left", formatter: this.formatIconsCount},
        {title: "Average", field: "avg", hozAlign: "left"},
      ]
    });
    this.createSvg();
    setTimeout(() => {
      this.http.get<ProtoDataResponse>('/api/wordle/get_season').subscribe((data) => {
        this.currentSeason = wordleDb.WordleSeason.decode(this.encoder.encode(data.data));
        this.selectedUser = `${this.credentials.getUserToken()!.user.id}`;
        this.statsTable?.setSort('gameId', 'desc');
        this.season = this.currentSeason.name;
      });
    }, 500);

  }

  private sortGameId(a: string, b: string, aRow: any, bRow: any, column: TabulatorNamespace.ColumnComponent, dir: string, sorterParams: any) {
    const aNumStr = StatsComponent.numberExtractor.exec(a) || ['0'];
    const bNumStr = StatsComponent.numberExtractor.exec(b) || ['0'];
    return Number.parseInt(aNumStr[0]) - Number.parseInt(bNumStr[0]);

  }

  private formatIconsCount(cell: TabulatorNamespace.CellComponent, formatterParams: {}, onRendered: any) {
    const data = cell.getData() as TableRowData;
    const identifier = [];
    for (let i = 1; i <= data.maxAttempts; i++) {

      identifier.push(i < (data.attempts > 0 ? data.attempts : data.maxAttempts) ? 'X' : 'O');
    }
    identifier.push(`(${data.attempts}/${data.maxAttempts})`)
    return `<span class="selfStatsRow">${identifier.join('')}</span>`
  }

  private createSvg(): void {
    this.svg = d3.select("figure#selfStats")
      .append("svg")
      .attr("width", this.width + (this.margin * 2))
      .attr("height", this.height + (this.margin * 2))
      .append("g");
    this.svg
      .attr("transform", "translate(" + this.margin + "," + this.margin + ")");
  }

  private fillStatsTable(user_id: string, avgData: AverageData): void {
    const selfRecord = this.currentSeason!.users[user_id];
    const tableData: Array<TableRowData> = [];
    Object.entries(selfRecord.classicGames).forEach(([key, value]) => {
      tableData.push({
        gameId: value.game,
        attempts: value.attempts,
        maxAttempts: value.maxAttempts,
        avg: avgData.data[value.game].total / avgData.data[value.game].counts,
        fails: avgData.data[value.game].fails
      })
    });
    this.statsTable!.setData(tableData).then(function () {
    })
      .catch(function (error) {
        console.log(error);
      });
  }

  private drawSeason(userId: string): void {
    if (this.currentSeason && userId) {
      const selfRecord = this.currentSeason.users[userId];
      if (!selfRecord || !this.svg) {
        return;
      }
      this.svgCanvas?.remove();
      this.svgCanvas = this.svg.append('g');

      const avgData: AverageData = {
        data: {}
      }
      let xCounts: { [key: string]: number } = {};
      let xKeys: Array<string> = [];
      let maxYVal = 5;
      this.availableUsers = [];
      Object.entries(this.currentSeason.users).forEach(([loopUserId, userRecord]) => {
        this.availableUsers.push({
          display: userRecord.lastKnownName,
          id: loopUserId
        })
        Object.entries(userRecord.classicGames).forEach(([gameId, gameRecord]) => {
          if (!(gameId in avgData)) {
            avgData.data[gameId] = {
              game_id: gameId,
              total: 0,
              fails: 0,
              counts: 0
            }
          }
          avgData.data[gameId].total += gameRecord.attempts >= 0 ? gameRecord.attempts : 0;
          avgData.data[gameId].fails += gameRecord.attempts < 0 ? 1 : 0;
          avgData.data[gameId].counts += 1;

          if (loopUserId == userId) {
            let itemKey = `${gameRecord.attempts}`;
            if (!(itemKey in xCounts)) {
              xCounts[itemKey] = 0;
              xKeys.push(itemKey);
            }
            xCounts[itemKey]++;
            if (xCounts[itemKey] >= maxYVal) {
              maxYVal = maxYVal + 5;
            }
          }
        });
      });
      xKeys.sort();

      this.fillStatsTable(userId, avgData);

      const x = d3.scaleBand()
        .range([0, this.width])
        .domain(xKeys)
        .padding(0.2);

      this.svgCanvas.append("g")
        .attr("transform", "translate(0," + this.height + ")")
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

      const y = d3.scaleLinear()
        .domain([0, maxYVal])
        .range([this.height, 0]);

      this.svgCanvas.append("g")
        .call(d3.axisLeft(y));

      this.svgCanvas.selectAll("bars")
        .data(Object.entries(xCounts).map(([key, val]) => {
          return {attempts: key, counts: val}
        }))
        .enter()
        .append("rect")
        .attr("x", d => x(d.attempts)!)
        .attr("y", d => y(d.counts))
        .attr("width", x.bandwidth())
        .attr("height", (d) => this.height - y(d.counts))
        .attr("fill", "#d04a35");


      this.svgCanvas.append("text")
        .attr("x", this.width / 2)
        .attr("y", 0)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .text("Attempt counts distribution");
    }

  }
}
