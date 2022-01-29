import {Component, OnInit} from '@angular/core';
import * as d3 from 'd3';
import * as wordleDb from '../../proto/WordlDb';
import {CredentialsProviderService} from "../credentials-provider.service";
import {HttpClient} from "@angular/common/http";

interface ProtoDataResponse {
  data: string;
}

interface AttemptsCount {
  attempts: string;
  counts: number;
}

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})
export class StatsComponent implements OnInit {
  private svg?: d3.Selection<SVGGElement, unknown, HTMLElement, any>;
  private margin = 50;
  private width = 750 - (this.margin * 2);
  private height = 400 - (this.margin * 2);
  private currentSeason?: wordleDb.WordleSeason;

  private readonly encoder: TextEncoder = new TextEncoder();

  constructor(private readonly credentials: CredentialsProviderService, private readonly http: HttpClient) {
  }

  ngOnInit(): void {
    this.createSvg();
    this.http.get<ProtoDataResponse>('/api/wordle/get_season').subscribe((data) => {
      this.currentSeason = wordleDb.WordleSeason.decode(this.encoder.encode(data.data));
      this.drawSeason();
    });
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

  private drawSeason(): void {
    if (this.currentSeason) {
      const selfRecord = this.currentSeason.users[this.credentials.getUserToken()!.user.id];
      if (!selfRecord || !this.svg) {
        return;
      }

      let xCounts: { [key: string]: number } = {};
      let xKeys: Array<string> = [];
      let maxYVal = 5;
      Object.entries(selfRecord.classicGames).forEach(([key, value]) => {
        let itemKey = `${value.attempts}`;
        if (!(itemKey in xCounts)) {
          xCounts[itemKey] = 0;
          xKeys.push(itemKey);
        }
        xCounts[itemKey]++;
        if (xCounts[itemKey] >= maxYVal) {
          maxYVal = maxYVal + 5;
        }
      });
      xKeys.sort();

      const x = d3.scaleBand()
        .range([0, this.width])
        .domain(xKeys)
        .padding(0.2);

      this.svg.append("g")
        .attr("transform", "translate(0," + this.height + ")")
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

      const y = d3.scaleLinear()
        .domain([0, maxYVal])
        .range([this.height, 0]);

      this.svg.append("g")
        .call(d3.axisLeft(y));

      this.svg.selectAll("bars")
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

      this.svg.append("text")
        .attr("x", this.width / 2)
        .attr("y", 0)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .text("Attempt counts");
    }

  }
}
