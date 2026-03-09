
import pygame as pg
import constants as con

class World():
    def __init__(self,mapImage,data):
         self.mapImage=mapImage
         self.data=data
         self.waypoints=[]
         self.tileMap=[]

    def ExtractData(self):
        #print(self.data)        
        for img in self.data:
            regions=self.data[img]["regions"]
            for region in regions:
                shape_attributes=region["shape_attributes"]
                all_points_x=shape_attributes["all_points_x"]
                all_points_y=shape_attributes["all_points_y"]
                self.waypoints=list(zip(all_points_x,all_points_y))


    def TileMap(self):
        for row in range(0,con.ROWS):
            self.tileMap.append([0]*con.COLS)
            
        for row in self.tileMap:
            print(row)
            
        startIndexX=int(self.waypoints[0][0]/con.tileSize)
        startIndexY=int(self.waypoints[0][1]/con.tileSize)
        for point in self.waypoints:
            endIndexX=int(point[0]/con.tileSize)
            endIndexY=int(point[1]/con.tileSize)
            print(startIndexX,startIndexY,endIndexX,endIndexY)
            """print(point)
            xIndex=int(point[0]/48)
            yIndex=int(point[1]/48)"""
            while startIndexX!=endIndexX:
                if startIndexX<endIndexX:
                    startIndexX+=1
                else:
                    startIndexX-=1
                self.tileMap[startIndexY][startIndexX]=1
                
            while startIndexY!=endIndexY:
                if startIndexY<endIndexY:
                    startIndexY+=1
                else:
                    startIndexY-=1
                self.tileMap[startIndexY][startIndexX]=1
                    


            self.tileMap[startIndexY][startIndexX]=1
            startIndexX=endIndexX
            startIndexY=endIndexY
            
        for row in self.tileMap:
            print(row)
