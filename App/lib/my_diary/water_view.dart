import 'package:best_flutter_ui_templates/ui_view/wave_view.dart';
import 'package:best_flutter_ui_templates/fitness_app_theme.dart';
import 'package:flutter/material.dart';

class WaterView extends StatefulWidget {
  const WaterView(
      {Key? key, this.mainScreenAnimationController, this.mainScreenAnimation})
      : super(key: key);

  final AnimationController? mainScreenAnimationController;
  final Animation<double>? mainScreenAnimation;

  @override
  _WaterViewState createState() => _WaterViewState();
}

class _WaterViewState extends State<WaterView> with TickerProviderStateMixin {
  Future<bool> getData() async {
    await Future<dynamic>.delayed(const Duration(milliseconds: 50));
    return true;
  }

  @override
  Widget build(BuildContext context) {

    final int percentage_bottle_value = 40;

    return AnimatedBuilder(
      animation: widget.mainScreenAnimationController!,
      builder: (BuildContext context, Widget? child) {
        return FadeTransition(
          opacity: widget.mainScreenAnimation!,
          child: Transform(
            transform: Matrix4.translationValues(
                0.0, 30 * (1.0 - widget.mainScreenAnimation!.value), 0.0),
            child: Padding(
              padding: const EdgeInsets.only(
                  left: 24, right: 24, top: 16, bottom: 18),
              child: Container(
                decoration: BoxDecoration(
                  color: FitnessAppTheme.white,
                  borderRadius: const BorderRadius.only(
                      topLeft: Radius.circular(8.0),
                      bottomLeft: Radius.circular(8.0),
                      bottomRight: Radius.circular(8.0),
                      topRight: Radius.circular(68.0)),
                  boxShadow: <BoxShadow>[
                    BoxShadow(
                        color: FitnessAppTheme.grey.withOpacity(0.2),
                        offset: const Offset(1.1, 1.1),
                        blurRadius: 10.0),
                  ],
                ),
                child: Padding(
                  padding: const EdgeInsets.only(
                      top: 16, left: 16, right: 16, bottom: 16),
                  child: Row(
                    children: <Widget>[
                      Expanded(
                        child: Column(
                          children: <Widget>[
                            Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: <Widget>[
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  crossAxisAlignment: CrossAxisAlignment.baseline, // baseline으로 설정
                                  textBaseline: TextBaseline.alphabetic, // 텍스트 기준선을 알파벳 기준으로 설정
                                  children: <Widget>[
                                    Padding(
                                      padding: const EdgeInsets.only(left: 4, bottom: 3),
                                      child: Row(
                                        crossAxisAlignment: CrossAxisAlignment.baseline,
                                        textBaseline: TextBaseline.alphabetic,
                                        children: <Widget>[
                                          Text(
                                            '일일 활동량:',
                                            textAlign: TextAlign.center,
                                            style: TextStyle(
                                              fontFamily: FitnessAppTheme.fontName,
                                              fontWeight: FontWeight.w600,
                                              fontSize: 25,
                                              color: FitnessAppTheme.nearlyDarkBlue,
                                            ),
                                          ),
                                          SizedBox(width: 4), // 텍스트 간 간격 조절
                                          Text(
                                            percentage_bottle_value > 50 ?
                                            '좋음':
                                            '나쁨',
                                            textAlign: TextAlign.center,
                                            style: TextStyle(
                                              fontFamily: FitnessAppTheme.fontName,
                                              fontWeight: FontWeight.w600,
                                              fontSize: 25,
                                              color: percentage_bottle_value > 50 ?
                                              FitnessAppTheme.nearlyDarkBlue :
                                              HexColor('#F65283'),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                                Padding(
                                  padding: const EdgeInsets.only(left: 4, top: 2, bottom: 14),
                                  child: Text(
                                    '더욱 운동이 필요합니다',
                                    textAlign: TextAlign.center,
                                    style: TextStyle(
                                      fontFamily: FitnessAppTheme.fontName,
                                      fontWeight: FontWeight.w500,
                                      fontSize: 14,
                                      letterSpacing: 0.0,
                                      color: FitnessAppTheme.darkText,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            Padding(
                              padding: const EdgeInsets.only(
                                  left: 4, right: 4, top: 8, bottom: 16),
                              child: Container(
                                height: 2,
                                decoration: BoxDecoration(
                                  color: FitnessAppTheme.background,
                                  borderRadius: const BorderRadius.all(
                                      Radius.circular(4.0)),
                                ),
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.only(top: 16),
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.end,
                                children: <Widget>[
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.start,
                                    crossAxisAlignment:
                                    CrossAxisAlignment.center,
                                    children: <Widget>[
                                      // Padding(
                                      //   padding: const EdgeInsets.only(left: 4),
                                      //   child: Icon(
                                      //     Icons.access_time,
                                      //     color: FitnessAppTheme.grey
                                      //         .withOpacity(0.5),
                                      //     size: 16,
                                      //   ),
                                      // ),



                                      // Padding(
                                      //   padding:
                                      //       const EdgeInsets.only(left: 4.0),
                                      //   child: Text(
                                      //     '가나다',
                                      //     textAlign: TextAlign.center,
                                      //     style: TextStyle(
                                      //       fontFamily:
                                      //           FitnessAppTheme.fontName,
                                      //       fontWeight: FontWeight.w500,
                                      //       fontSize: 14,
                                      //       letterSpacing: 0.0,
                                      //       color: FitnessAppTheme.grey
                                      //           .withOpacity(0.5),
                                      //     ),
                                      //   ),
                                      // ),
                                    ],
                                  ),



                                  // Padding(
                                  //   padding: const EdgeInsets.only(top: 4),
                                  //   child: Row(
                                  //     mainAxisAlignment:
                                  //         MainAxisAlignment.start,
                                  //     crossAxisAlignment:
                                  //         CrossAxisAlignment.center,
                                  //     children: <Widget>[
                                  //       SizedBox(
                                  //         width: 24,
                                  //         height: 24,
                                  //         child: Image.asset(
                                  //             'assets/fitness_app/bell.png'),
                                  //       ),
                                  //       Flexible(
                                  //         child: Text(
                                  //           '건강 bottle을 채워봅시다!',
                                  //           textAlign: TextAlign.start,
                                  //           style: TextStyle(
                                  //             fontFamily:
                                  //                 FitnessAppTheme.fontName,
                                  //             fontWeight: FontWeight.w500,
                                  //             fontSize: 12,
                                  //             letterSpacing: 0.0,
                                  //             color: HexColor('#F65283'),
                                  //           ),
                                  //         ),
                                  //       ),
                                  //     ],
                                  //   ),
                                  // ),
                                ],
                              ),
                            )
                          ],
                        ),
                      ),
                      SizedBox(
                        width: 34,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: <Widget>[
                            Container(
                              decoration: BoxDecoration(
                                color: FitnessAppTheme.nearlyWhite,
                                shape: BoxShape.circle,
                                boxShadow: <BoxShadow>[
                                  BoxShadow(
                                      color: FitnessAppTheme.nearlyDarkBlue
                                          .withOpacity(0.4),
                                      offset: const Offset(4.0, 4.0),
                                      blurRadius: 8.0),
                                ],
                              ),
                              // child: Padding(
                              //   padding: const EdgeInsets.all(6.0),
                              //   child: Icon(
                              //     Icons.add,
                              //     color: FitnessAppTheme.nearlyDarkBlue,
                              //     size: 24,
                              //   ),
                              // ),
                            ),
                            const SizedBox(
                              height: 28,
                            ),
                            Container(
                              decoration: BoxDecoration(
                                color: FitnessAppTheme.nearlyWhite,
                                shape: BoxShape.circle,
                                boxShadow: <BoxShadow>[
                                  BoxShadow(
                                      color: FitnessAppTheme.nearlyDarkBlue
                                          .withOpacity(0.4),
                                      offset: const Offset(4.0, 4.0),
                                      blurRadius: 8.0),
                                ],
                              ),
                              // child: Padding(
                              //   padding: const EdgeInsets.all(6.0),
                              //   child: Icon(
                              //     Icons.remove,
                              //     color: FitnessAppTheme.nearlyDarkBlue,
                              //     size: 24,
                              //   ),
                              // ),
                            ),
                          ],
                        ),
                      ),
                      Padding(
                        padding:
                        const EdgeInsets.only(left: 16, right: 8, top: 16),
                        child: Container(
                          width: 60,
                          height: 160,
                          decoration: BoxDecoration(
                            color: HexColor('#E8EDFE'),
                            borderRadius: const BorderRadius.only(
                                topLeft: Radius.circular(80.0),
                                bottomLeft: Radius.circular(80.0),
                                bottomRight: Radius.circular(80.0),
                                topRight: Radius.circular(80.0)),
                            boxShadow: <BoxShadow>[
                              BoxShadow(
                                  color: FitnessAppTheme.grey.withOpacity(0.4),
                                  offset: const Offset(2, 2),
                                  blurRadius: 4),
                            ],
                          ),
                          child: WaveView(
                            percentageValue: percentage_bottle_value.toDouble(),
                          ),
                        ),
                      )
                    ],
                  ),
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}
