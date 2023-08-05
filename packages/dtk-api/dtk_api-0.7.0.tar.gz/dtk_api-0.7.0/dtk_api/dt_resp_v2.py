from typing import List, Any, Optional, Union

from pydantic import BaseModel, Field


class CategoryGetSuperCategoryRespSubcategories(BaseModel):
    subcid: Optional[int] = Field(None)
    subcname: Optional[str] = Field(None)
    scpic: Optional[str] = Field(None)


class CategoryGetSuperCategoryResp(BaseModel):
    cid: Optional[Union[int, float]] = Field(None)
    cname: Optional[str] = Field(None)
    cpic: Optional[str] = Field(None)
    subcategories: Optional[List[CategoryGetSuperCategoryRespSubcategories]] = Field(
        None
    )


class GoodsPriceTrendRespHistoricalprice(BaseModel):
    actualPrice: Optional[float] = Field(None)
    date: Optional[str] = Field(None)


class GoodsPriceTrendResp(BaseModel):
    id: Optional[Union[int, float]] = Field(None)
    goodsId: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    dtitle: Optional[str] = Field(None)
    originalPrice: Optional[float] = Field(None)
    historicalPrice: Optional[List[GoodsPriceTrendRespHistoricalprice]] = Field(None)
    monthSales: Optional[Union[int, float]] = Field(None)
    twoHoursSales: Optional[Union[int, float]] = Field(None)
    dailySales: Optional[Union[int, float]] = Field(None)
    commissionType: Optional[Union[int, float]] = Field(None)
    desc: Optional[str] = Field(None)
    couponReceiveNum: Optional[Union[int, float]] = Field(None)
    couponEndTime: Optional[str] = Field(None)
    couponStartTime: Optional[str] = Field(None)
    couponPrice: Optional[float] = Field(None)
    couponConditions: Optional[str] = Field(None)
    mainPic: Optional[str] = Field(None)
    marketingMainPic: Optional[str] = Field(None)
    commissionRate: Optional[float] = Field(None)
    couponTotalNum: Optional[Union[int, float]] = Field(None)
    brandId: Optional[Union[int, float]] = Field(None)
    brandName: Optional[str] = Field(None)
    itemLink: Optional[str] = Field(None)


class GoodsGetDtkSearchGoodsRespList(BaseModel):
    id: Optional[int] = Field(None)
    goodsId: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    dtitle: Optional[str] = Field(None)
    originalPrice: Optional[float] = Field(None)
    actualPrice: Optional[float] = Field(None)
    shopType: Optional[int] = Field(None)
    goldSellers: Optional[int] = Field(None)
    monthSales: Optional[int] = Field(None)
    twoHoursSales: Optional[int] = Field(None)
    dailySales: Optional[int] = Field(None)
    commissionType: Optional[int] = Field(None)
    desc: Optional[str] = Field(None)
    couponReceiveNum: Optional[int] = Field(None)
    couponLink: Optional[str] = Field(None)
    couponEndTime: Optional[str] = Field(None)
    couponStartTime: Optional[str] = Field(None)
    couponPrice: Optional[float] = Field(None)
    couponConditions: Optional[str] = Field(None)
    activityType: Optional[int] = Field(None)
    createTime: Optional[str] = Field(None)
    mainPic: Optional[str] = Field(None)
    marketingMainPic: Optional[str] = Field(None)
    sellerId: Optional[str] = Field(None)
    cid: Optional[int] = Field(None)
    discounts: Optional[float] = Field(None)
    commissionRate: Optional[float] = Field(None)
    couponTotalNum: Optional[int] = Field(None)
    haitao: Optional[int] = Field(None)
    activityStartTime: Optional[str] = Field(None)
    activityEndTime: Optional[str] = Field(None)
    shopName: Optional[str] = Field(None)
    shopLevel: Optional[int] = Field(None)
    descScore: Optional[float] = Field(None)
    brand: Optional[int] = Field(None)
    brandId: Optional[int] = Field(None)
    brandName: Optional[str] = Field(None)
    hotPush: Optional[int] = Field(None)
    teamName: Optional[str] = Field(None)
    itemLink: Optional[str] = Field(None)
    tchaoshi: Optional[int] = Field(None)
    dsrScore: Optional[float] = Field(None)
    dsrPercent: Optional[float] = Field(None)
    shipScore: Optional[float] = Field(None)
    shipPercent: Optional[float] = Field(None)
    serviceScore: Optional[float] = Field(None)
    servicePercent: Optional[float] = Field(None)
    subcid: Optional[list] = Field(None)
    quanMLink: Optional[int] = Field(None)
    hzQuanOver: Optional[int] = Field(None)
    yunfeixian: Optional[int] = Field(None)
    estimateAmount: Optional[int] = Field(None)
    freeshipRemoteDistrict: Optional[int] = Field(None)
    tbcid: Optional[int] = Field(None)


class GoodsGetDtkSearchGoodsResp(BaseModel):
    list: Optional[List[GoodsGetDtkSearchGoodsRespList]] = Field(None)
    totalNum: Optional[Union[int, float]] = Field(None)
    pageId: Optional[str] = Field(None)


class TbServiceGetPrivilegeLinkResp(BaseModel):
    couponClickUrl: Optional[str] = Field(None)
    couponEndTime: Optional[str] = Field(None)
    couponInfo: Optional[str] = Field(None)
    couponStartTime: Optional[str] = Field(None)
    itemId: Optional[str] = Field(None)
    couponTotalCount: Optional[str] = Field(None)
    couponRemainCount: Optional[str] = Field(None)
    itemUrl: Optional[str] = Field(None)
    tpwd: Optional[str] = Field(None)
    maxCommissionRate: Optional[str] = Field(None)
    shortUrl: Optional[str] = Field(None)
    minCommissionRate: Optional[str] = Field(None)
    longTpwd: Optional[str] = Field(None)


class GoodsGetRankingListResp(BaseModel):
    id: Optional[Union[int, float]] = Field(None)
    goodsId: Optional[str] = Field(None)
    ranking: Optional[Union[int, float]] = Field(None)
    dtitle: Optional[str] = Field(None)
    actualPrice: Optional[float] = Field(None)
    commissionRate: Optional[float] = Field(None)
    couponPrice: Optional[float] = Field(None)
    couponReceiveNum: Optional[Union[int, float]] = Field(None)
    couponTotalNum: Optional[Union[int, float]] = Field(None)
    monthSales: Optional[Union[int, float]] = Field(None)
    twoHoursSales: Optional[Union[int, float]] = Field(None)
    dailySales: Optional[Union[int, float]] = Field(None)
    hotPush: Optional[Union[int, float]] = Field(None)
    mainPic: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    desc: Optional[str] = Field(None)
    originalPrice: Optional[float] = Field(None)
    couponLink: Optional[str] = Field(None)
    couponStartTime: Optional[str] = Field(None)
    couponEndTime: Optional[str] = Field(None)
    commissionType: Optional[Union[int, float]] = Field(None)
    createTime: Optional[str] = Field(None)
    activityType: Optional[Union[int, float]] = Field(None)
    imgs: Optional[str] = Field(None)
    guideName: Optional[str] = Field(None)
    shopType: Optional[Union[int, float]] = Field(None)
    couponConditions: Optional[str] = Field(None)
    newRankingGoods: Optional[Union[int, float]] = Field(None)
    sellerId: Optional[str] = Field(None)
    quanMLink: Optional[Union[int, float]] = Field(None)
    hzQuanOver: Optional[Union[int, float]] = Field(None)
    yunfeixian: Optional[Union[int, float]] = Field(None)
    estimateAmount: Optional[Union[int, float]] = Field(None)
    freeshipRemoteDistrict: Optional[Union[int, float]] = Field(None)


class GoodsGetGoodsDetailsResp(BaseModel):
    id: Optional[Union[int, float]] = Field(None)
    goodsId: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    dtitle: Optional[str] = Field(None)
    originalPrice: Optional[float] = Field(None)
    actualPrice: Optional[float] = Field(None)
    shopType: Optional[Union[int, float]] = Field(None)
    goldSellers: Optional[Union[int, float]] = Field(None)
    monthSales: Optional[Union[int, float]] = Field(None)
    twoHoursSales: Optional[Union[int, float]] = Field(None)
    dailySales: Optional[Union[int, float]] = Field(None)
    commissionType: Optional[Union[int, float]] = Field(None)
    desc: Optional[str] = Field(None)
    couponReceiveNum: Optional[Union[int, float]] = Field(None)
    couponLink: Optional[str] = Field(None)
    couponEndTime: Optional[str] = Field(None)
    couponStartTime: Optional[str] = Field(None)
    couponPrice: Optional[float] = Field(None)
    couponConditions: Optional[str] = Field(None)
    activityType: Optional[Union[int, float]] = Field(None)
    createTime: Optional[str] = Field(None)
    mainPic: Optional[str] = Field(None)
    marketingMainPic: Optional[str] = Field(None)
    sellerId: Optional[str] = Field(None)
    brandWenan: Optional[str] = Field(None)
    cid: Optional[Union[int, float]] = Field(None)
    discounts: Optional[float] = Field(None)
    commissionRate: Optional[float] = Field(None)
    couponTotalNum: Optional[Union[int, float]] = Field(None)
    haitao: Optional[Union[int, float]] = Field(None)
    activityStartTime: Optional[str] = Field(None)
    activityEndTime: Optional[str] = Field(None)
    shopName: Optional[str] = Field(None)
    shopLevel: Optional[Union[int, float]] = Field(None)
    descScore: Optional[float] = Field(None)
    brand: Optional[Union[int, float]] = Field(None)
    brandId: Optional[Union[int, float]] = Field(None)
    brandName: Optional[str] = Field(None)
    hotPush: Optional[Union[int, float]] = Field(None)
    teamName: Optional[str] = Field(None)
    itemLink: Optional[str] = Field(None)
    tchaoshi: Optional[Union[int, float]] = Field(None)
    dsrScore: Optional[float] = Field(None)
    dsrPercent: Optional[float] = Field(None)
    shipScore: Optional[float] = Field(None)
    shipPercent: Optional[float] = Field(None)
    serviceScore: Optional[float] = Field(None)
    servicePercent: Optional[float] = Field(None)
    subcid: Optional[list] = Field(None)
    imgs: Optional[str] = Field(None)
    reimgs: Optional[str] = Field(None)
    quanMLink: Optional[Union[int, float]] = Field(None)
    hzQuanOver: Optional[Union[int, float]] = Field(None)
    yunfeixian: Optional[Union[int, float]] = Field(None)
    estimateAmount: Optional[Union[int, float]] = Field(None)
    shopLogo: Optional[str] = Field(None)
    specialText: Optional[list] = Field(None)
    freeshipRemoteDistrict: Optional[Union[int, float]] = Field(None)
    video: Optional[str] = Field(None)
    detailPics: Optional[str] = Field(None)
    isSubdivision: Optional[Union[int, float]] = Field(None)
    subdivisionId: Optional[Union[int, float]] = Field(None)
    subdivisionName: Optional[str] = Field(None)
    subdivisionRank: Optional[Union[int, float]] = Field(None)
    tbcid: Optional[Union[int, float]] = Field(None)


class TbServiceGetBrandListRespShop(BaseModel):
    name: Optional[str] = Field(None)
    sellerId: Optional[str] = Field(None)


class TbServiceGetBrandListResp(BaseModel):
    cid: Optional[Union[int, float]] = Field(None)
    brandId: Optional[Union[int, float]] = Field(None)
    brandName: Optional[str] = Field(None)
    brandLogo: Optional[str] = Field(None)
    brandEnglish: Optional[str] = Field(None)
    shop: Optional[List[TbServiceGetBrandListRespShop]] = Field(None)
    brandScore: Optional[Union[int, float]] = Field(None)
    location: Optional[str] = Field(None)
    establishTime: Optional[str] = Field(None)
    belongTo: Optional[str] = Field(None)
    position: Optional[str] = Field(None)
    consumer: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    simpleLabel: Optional[str] = Field(None)
    cids: Optional[str] = Field(None)
    sales2h: Optional[Union[int, float]] = Field(None)
    fansNum: Optional[Union[int, float]] = Field(None)
    brandDesc: Optional[str] = Field(None)


class GoodsNineOpGoodsListRespList(BaseModel):
    id: Optional[int] = Field(None)
    goodsId: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    dtitle: Optional[str] = Field(None)
    originalPrice: Optional[float] = Field(None)
    actualPrice: Optional[float] = Field(None)
    shopType: Optional[int] = Field(None)
    goldSellers: Optional[int] = Field(None)
    monthSales: Optional[int] = Field(None)
    twoHoursSales: Optional[int] = Field(None)
    dailySales: Optional[int] = Field(None)
    commissionType: Optional[int] = Field(None)
    desc: Optional[str] = Field(None)
    couponReceiveNum: Optional[int] = Field(None)
    couponLink: Optional[str] = Field(None)
    couponEndTime: Optional[str] = Field(None)
    couponStartTime: Optional[str] = Field(None)
    couponPrice: Optional[float] = Field(None)
    couponConditions: Optional[str] = Field(None)
    activityType: Optional[int] = Field(None)
    createTime: Optional[str] = Field(None)
    mainPic: Optional[str] = Field(None)
    marketingMainPic: Optional[str] = Field(None)
    sellerId: Optional[str] = Field(None)
    brandWenan: Optional[str] = Field(None)
    cid: Optional[int] = Field(None)
    discounts: Optional[float] = Field(None)
    commissionRate: Optional[float] = Field(None)
    couponTotalNum: Optional[int] = Field(None)
    haitao: Optional[int] = Field(None)
    activityStartTime: Optional[str] = Field(None)
    activityEndTime: Optional[str] = Field(None)
    shopName: Optional[str] = Field(None)
    shopLevel: Optional[int] = Field(None)
    descScore: Optional[float] = Field(None)
    brand: Optional[int] = Field(None)
    brandId: Optional[int] = Field(None)
    brandName: Optional[str] = Field(None)
    hotPush: Optional[int] = Field(None)
    teamName: Optional[str] = Field(None)
    itemLink: Optional[str] = Field(None)
    tchaoshi: Optional[int] = Field(None)
    dsrScore: Optional[float] = Field(None)
    dsrPercent: Optional[float] = Field(None)
    shipScore: Optional[float] = Field(None)
    shipPercent: Optional[float] = Field(None)
    serviceScore: Optional[float] = Field(None)
    servicePercent: Optional[float] = Field(None)
    subcid: Optional[list] = Field(None)
    nineCid: Optional[int] = Field(None)
    quanMLink: Optional[int] = Field(None)
    hzQuanOver: Optional[int] = Field(None)
    yunfeixian: Optional[int] = Field(None)
    estimateAmount: Optional[int] = Field(None)
    freeshipRemoteDistrict: Optional[int] = Field(None)
    video: Optional[str] = Field(None)
    tbcid: Optional[int] = Field(None)


class GoodsNineOpGoodsListResp(BaseModel):
    list: Optional[List[GoodsNineOpGoodsListRespList]] = Field(None)
    totalNum: Optional[Union[int, float]] = Field(None)
    pageId: Optional[str] = Field(None)


class TbServiceGetTbServiceRespSmall_images(BaseModel):
    string: Optional[List[str]] = Field(None)


class TbServiceGetTbServiceResp(BaseModel):
    title: Optional[str] = Field(None)
    volume: Optional[Union[int, float]] = Field(None)
    nick: Optional[str] = Field(None)
    coupon_start_time: Optional[str] = Field(None)
    coupon_end_time: Optional[str] = Field(None)
    tk_total_sales: Optional[str] = Field(None)
    coupon_id: Optional[str] = Field(None)
    pict_url: Optional[str] = Field(None)
    small_images: Optional[TbServiceGetTbServiceRespSmall_images] = Field(None)
    reserve_price: Optional[str] = Field(None)
    zk_final_price: Optional[str] = Field(None)
    user_type: Optional[Union[int, float]] = Field(None)
    commission_rate: Optional[str] = Field(None)
    seller_id: Optional[Union[int, float]] = Field(None)
    coupon_total_count: Optional[Union[int, float]] = Field(None)
    coupon_remain_count: Optional[Union[int, float]] = Field(None)
    coupon_info: Optional[str] = Field(None)
    shop_title: Optional[str] = Field(None)
    shop_dsr: Optional[Union[int, float]] = Field(None)
    level_one_category_name: Optional[str] = Field(None)
    level_one_category_id: Optional[Union[int, float]] = Field(None)
    category_name: Optional[str] = Field(None)
    category_id: Optional[Union[int, float]] = Field(None)
    short_title: Optional[str] = Field(None)
    white_image: Optional[str] = Field(None)
    coupon_start_fee: Optional[str] = Field(None)
    coupon_amount: Optional[str] = Field(None)
    item_description: Optional[str] = Field(None)
    item_id: Optional[Union[int, float]] = Field(None)
    ysyl_tlj_face: Optional[Union[int, float]] = Field(None)
    presale_deposit: Optional[Union[int, float]] = Field(None)
    presale_discount_fee_text: Optional[str] = Field(None)


class CategoryGetTop100Resp(BaseModel):
    hotWords: Optional[List[str]] = Field(None)


class GoodsGetGoodsListResp(BaseModel):
    id: Optional[Union[int, float]] = Field(None)
    goodsId: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    dtitle: Optional[str] = Field(None)
    originalPrice: Optional[float] = Field(None)
    actualPrice: Optional[float] = Field(None)
    shopType: Optional[Union[int, float]] = Field(None)
    goldSellers: Optional[Union[int, float]] = Field(None)
    monthSales: Optional[Union[int, float]] = Field(None)
    twoHoursSales: Optional[Union[int, float]] = Field(None)
    dailySales: Optional[Union[int, float]] = Field(None)
    commissionType: Optional[Union[int, float]] = Field(None)
    desc: Optional[str] = Field(None)
    couponReceiveNum: Optional[Union[int, float]] = Field(None)
    couponLink: Optional[str] = Field(None)
    couponEndTime: Optional[str] = Field(None)
    couponStartTime: Optional[str] = Field(None)
    couponPrice: Optional[float] = Field(None)
    couponConditions: Optional[str] = Field(None)
    activityType: Optional[Union[int, float]] = Field(None)
    createTime: Optional[str] = Field(None)
    mainPic: Optional[str] = Field(None)
    marketingMainPic: Optional[str] = Field(None)
    sellerId: Optional[str] = Field(None)
    brandWenan: Optional[str] = Field(None)
    cid: Optional[Union[int, float]] = Field(None)
    discounts: Optional[float] = Field(None)
    commissionRate: Optional[float] = Field(None)
    couponTotalNum: Optional[Union[int, float]] = Field(None)
    haitao: Optional[Union[int, float]] = Field(None)
    activityStartTime: Optional[str] = Field(None)
    activityEndTime: Optional[str] = Field(None)
    shopName: Optional[str] = Field(None)
    shopLevel: Optional[Union[int, float]] = Field(None)
    descScore: Optional[float] = Field(None)
    brand: Optional[Union[int, float]] = Field(None)
    brandId: Optional[Union[int, float]] = Field(None)
    brandName: Optional[str] = Field(None)
    hotPush: Optional[Union[int, float]] = Field(None)
    teamName: Optional[str] = Field(None)
    itemLink: Optional[str] = Field(None)
    tchaoshi: Optional[Union[int, float]] = Field(None)
    dsrScore: Optional[float] = Field(None)
    dsrPercent: Optional[float] = Field(None)
    shipScore: Optional[float] = Field(None)
    shipPercent: Optional[float] = Field(None)
    serviceScore: Optional[float] = Field(None)
    servicePercent: Optional[float] = Field(None)
    subcid: Optional[List[int]] = Field(None)
    quanMLink: Optional[Union[int, float]] = Field(None)
    hzQuanOver: Optional[Union[int, float]] = Field(None)
    yunfeixian: Optional[Union[int, float]] = Field(None)
    estimateAmount: Optional[Union[int, float]] = Field(None)
    shopLogo: Optional[str] = Field(None)
    specialText: Optional[List[str]] = Field(None)
    freeshipRemoteDistrict: Optional[Union[int, float]] = Field(None)
    video: Optional[str] = Field(None)
    tbcid: Optional[Union[int, float]] = Field(None)


class GoodsListSuperGoodsResp(BaseModel):
    id: Optional[Union[int, float]] = Field(None)
    goodsId: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    dtitle: Optional[str] = Field(None)
    originalPrice: Optional[float] = Field(None)
    actualPrice: Optional[float] = Field(None)
    shopType: Optional[Union[int, float]] = Field(None)
    goldSellers: Optional[Union[int, float]] = Field(None)
    monthSales: Optional[Union[int, float]] = Field(None)
    twoHoursSales: Optional[Union[int, float]] = Field(None)
    dailySales: Optional[Union[int, float]] = Field(None)
    commissionType: Optional[Union[int, float]] = Field(None)
    desc: Optional[str] = Field(None)
    couponReceiveNum: Optional[Union[int, float]] = Field(None)
    couponLink: Optional[str] = Field(None)
    couponEndTime: Optional[str] = Field(None)
    couponStartTime: Optional[str] = Field(None)
    couponPrice: Optional[float] = Field(None)
    couponConditions: Optional[str] = Field(None)
    activityType: Optional[Union[int, float]] = Field(None)
    createTime: Optional[str] = Field(None)
    mainPic: Optional[str] = Field(None)
    marketingMainPic: Optional[str] = Field(None)
    sellerId: Optional[str] = Field(None)
    brandWenan: Optional[str] = Field(None)
    cid: Optional[Union[int, float]] = Field(None)
    discounts: Optional[float] = Field(None)
    commissionRate: Optional[float] = Field(None)
    couponTotalNum: Optional[Union[int, float]] = Field(None)
    haitao: Optional[Union[int, float]] = Field(None)
    activityStartTime: Optional[str] = Field(None)
    activityEndTime: Optional[str] = Field(None)
    shopName: Optional[str] = Field(None)
    shopLevel: Optional[Union[int, float]] = Field(None)
    descScore: Optional[float] = Field(None)
    brand: Optional[Union[int, float]] = Field(None)
    brandId: Optional[Union[int, float]] = Field(None)
    brandName: Optional[str] = Field(None)
    hotPush: Optional[Union[int, float]] = Field(None)
    teamName: Optional[str] = Field(None)
    itemLink: Optional[str] = Field(None)
    tchaoshi: Optional[Union[int, float]] = Field(None)
    dsrScore: Optional[float] = Field(None)
    dsrPercent: Optional[float] = Field(None)
    shipScore: Optional[float] = Field(None)
    shipPercent: Optional[float] = Field(None)
    serviceScore: Optional[float] = Field(None)
    servicePercent: Optional[float] = Field(None)
    subcid: Optional[List[int]] = Field(None)
    quanMLink: Optional[Union[int, float]] = Field(None)
    hzQuanOver: Optional[Union[int, float]] = Field(None)
    yunfeixian: Optional[Union[int, float]] = Field(None)
    estimateAmount: Optional[Union[int, float]] = Field(None)
    tbcid: Optional[Union[int, float]] = Field(None)


class GoodsListSimilerGoodsByOpenResp(BaseModel):
    id: Optional[Union[int, float]] = Field(None)
    goodsId: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    dtitle: Optional[str] = Field(None)
    originalPrice: Optional[float] = Field(None)
    actualPrice: Optional[float] = Field(None)
    shopType: Optional[Union[int, float]] = Field(None)
    goldSellers: Optional[Union[int, float]] = Field(None)
    monthSales: Optional[Union[int, float]] = Field(None)
    twoHoursSales: Optional[Union[int, float]] = Field(None)
    dailySales: Optional[Union[int, float]] = Field(None)
    commissionType: Optional[Union[int, float]] = Field(None)
    desc: Optional[str] = Field(None)
    couponReceiveNum: Optional[Union[int, float]] = Field(None)
    couponLink: Optional[str] = Field(None)
    couponEndTime: Optional[str] = Field(None)
    couponStartTime: Optional[str] = Field(None)
    couponPrice: Optional[float] = Field(None)
    couponConditions: Optional[str] = Field(None)
    activityType: Optional[Union[int, float]] = Field(None)
    createTime: Optional[str] = Field(None)
    mainPic: Optional[str] = Field(None)
    marketingMainPic: Optional[str] = Field(None)
    sellerId: Optional[str] = Field(None)
    brandWenan: Optional[str] = Field(None)
    cid: Optional[Union[int, float]] = Field(None)
    discounts: Optional[float] = Field(None)
    commissionRate: Optional[float] = Field(None)
    couponTotalNum: Optional[Union[int, float]] = Field(None)
    haitao: Optional[Union[int, float]] = Field(None)
    activityStartTime: Optional[str] = Field(None)
    activityEndTime: Optional[str] = Field(None)
    shopName: Optional[str] = Field(None)
    shopLevel: Optional[Union[int, float]] = Field(None)
    descScore: Optional[float] = Field(None)
    brand: Optional[Union[int, float]] = Field(None)
    brandId: Optional[Union[int, float]] = Field(None)
    brandName: Optional[str] = Field(None)
    hotPush: Optional[Union[int, float]] = Field(None)
    teamName: Optional[str] = Field(None)
    itemLink: Optional[str] = Field(None)
    tchaoshi: Optional[Union[int, float]] = Field(None)
    dsrScore: Optional[float] = Field(None)
    dsrPercent: Optional[float] = Field(None)
    shipScore: Optional[float] = Field(None)
    shipPercent: Optional[float] = Field(None)
    serviceScore: Optional[float] = Field(None)
    servicePercent: Optional[float] = Field(None)
    subcid: Optional[List[int]] = Field(None)
    quanMLink: Optional[Union[int, float]] = Field(None)
    hzQuanOver: Optional[Union[int, float]] = Field(None)
    yunfeixian: Optional[Union[int, float]] = Field(None)
    estimateAmount: Optional[Union[int, float]] = Field(None)
    freeshipRemoteDistrict: Optional[Union[int, float]] = Field(None)
    tbcid: Optional[Union[int, float]] = Field(None)


class GoodsSearchSuggestionResp(BaseModel):
    kw: Optional[str] = Field(None)
    total: Optional[Union[int, float]] = Field(None)


class GoodsActivityCatalogueResp(BaseModel):
    activityId: Optional[Union[int, float]] = Field(None)
    activityName: Optional[str] = Field(None)
    startTime: Optional[str] = Field(None)
    endTime: Optional[str] = Field(None)
    goodsLabel: Optional[str] = Field(None)
    detailLabel: Optional[str] = Field(None)
    goodsType: Optional[Union[int, float]] = Field(None)


class GoodsTopicCatalogueResp(BaseModel):
    topicId: Optional[Union[int, float]] = Field(None)
    topicName: Optional[str] = Field(None)
    startTime: Optional[str] = Field(None)
    endTime: Optional[str] = Field(None)
    banner: Optional[List[str]] = Field(None)
    topBanner: Optional[List[str]] = Field(None)


class CategoryDdqGoodsListRespGoodslist(BaseModel):
    id: Optional[int] = Field(None)
    goodsId: Optional[str] = Field(None)
    itemLink: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    dtitle: Optional[str] = Field(None)
    cid: Optional[int] = Field(None)
    subcid: Optional[List[int]] = Field(None)
    ddqDesc: Optional[str] = Field(None)
    mainPic: Optional[str] = Field(None)
    originalPrice: Optional[float] = Field(None)
    actualPrice: Optional[float] = Field(None)
    couponPrice: Optional[float] = Field(None)
    discounts: Optional[float] = Field(None)
    couponLink: Optional[str] = Field(None)
    couponEndTime: Optional[str] = Field(None)
    couponStartTime: Optional[str] = Field(None)
    couponConditions: Optional[str] = Field(None)
    commissionType: Optional[int] = Field(None)
    commissionRate: Optional[float] = Field(None)
    createTime: Optional[str] = Field(None)
    couponReceiveNum: Optional[int] = Field(None)
    couponTotalNum: Optional[int] = Field(None)
    monthSales: Optional[int] = Field(None)
    activityType: Optional[int] = Field(None)
    activityStartTime: Optional[str] = Field(None)
    activityEndTime: Optional[str] = Field(None)
    shopName: Optional[str] = Field(None)
    shopLevel: Optional[int] = Field(None)
    sellerId: Optional[str] = Field(None)
    brand: Optional[int] = Field(None)
    brandId: Optional[int] = Field(None)
    brandName: Optional[str] = Field(None)
    twoHoursSales: Optional[int] = Field(None)
    dailySales: Optional[int] = Field(None)
    quanMLink: Optional[int] = Field(None)
    hzQuanOver: Optional[int] = Field(None)
    yunfeixian: Optional[int] = Field(None)
    estimateAmount: Optional[int] = Field(None)
    marketingMainPic: Optional[str] = Field(None)
    tbcid: Optional[int] = Field(None)


class CategoryDdqGoodsListRespRoundslist(BaseModel):
    ddqTime: Optional[str] = Field(None)
    status: Optional[int] = Field(None)


class CategoryDdqGoodsListResp(BaseModel):
    ddqTime: Optional[str] = Field(None)
    status: Optional[Union[int, float]] = Field(None)
    goodsList: Optional[List[CategoryDdqGoodsListRespGoodslist]] = Field(None)
    roundsList: Optional[List[CategoryDdqGoodsListRespRoundslist]] = Field(None)


class TbServiceParseTaokoulingRespOrigininfo(BaseModel):
    activityId: Optional[str] = Field(None)
    actualPrice: Optional[int] = Field(None)
    amount: Optional[int] = Field(None)
    endTime: Optional[str] = Field(None)
    image: Optional[str] = Field(None)
    pid: Optional[str] = Field(None)
    price: Optional[int] = Field(None)
    shopLogo: Optional[str] = Field(None)
    shopName: Optional[str] = Field(None)
    startFee: Optional[int] = Field(None)
    startTime: Optional[str] = Field(None)
    status: Optional[int] = Field(None)
    title: Optional[str] = Field(None)


class TbServiceParseTaokoulingResp(BaseModel):
    commissionRate: Optional[Union[int, float]] = Field(None)
    commissionType: Optional[str] = Field(None)
    goodsId: Optional[str] = Field(None)
    originInfo: Optional[TbServiceParseTaokoulingRespOrigininfo] = Field(None)
    originType: Optional[str] = Field(None)
    originUrl: Optional[str] = Field(None)


class TbServiceCreatTaokoulingResp(BaseModel):
    password_simple: Optional[str] = Field(None)
    model: Optional[str] = Field(None)
    longTpwd: Optional[str] = Field(None)


class GoodsExclusiveGoodsListResp(BaseModel):
    id: int = Field(...)
    goodsId: str = Field(...)
    title: str = Field(...)
    dtitle: str = Field(...)
    originalPrice: float = Field(...)
    actualPrice: float = Field(...)
    shopType: int = Field(...)
    goldSellers: int = Field(...)
    monthSales: int = Field(...)
    twoHoursSales: int = Field(...)
    dailySales: int = Field(...)
    commissionType: int = Field(...)
    desc: str = Field(...)
    couponReceiveNum: int = Field(...)
    couponLink: str = Field(...)
    couponEndTime: str = Field(...)
    couponStartTime: str = Field(...)
    couponPrice: float = Field(...)
    couponConditions: str = Field(...)
    activityType: int = Field(...)
    createTime: str = Field(...)
    mainPic: str = Field(...)
    marketingMainPic: str = Field(...)
    sellerId: str = Field(...)
    cid: int = Field(...)
    discounts: float = Field(...)
    commissionRate: float = Field(...)
    couponTotalNum: int = Field(...)
    activityStartTime: str = Field(...)
    activityEndTime: str = Field(...)
    shopName: str = Field(...)
    shopLevel: int = Field(...)
    descScore: float = Field(...)
    brand: int = Field(...)
    brandId: int = Field(...)
    brandName: str = Field(...)
    hotPush: int = Field(...)
    teamName: str = Field(...)
    itemLink: str = Field(...)
    tchaoshi: int = Field(...)
    dsrScore: float = Field(...)
    dsrPercent: float = Field(...)
    shipScore: float = Field(...)
    shipPercent: float = Field(...)
    serviceScore: float = Field(...)
    servicePercent: float = Field(...)
    subcid: List[int] = Field(...)
    video: str = Field(...)
    quanMLink: int = Field(...)
    hzQuanOver: int = Field(...)
    yunfeixian: int = Field(...)
    estimateAmount: int = Field(...)
    freeshipRemoteDistrict: int = Field(...)
    specialText: list = Field(...)
    tbcid: int = Field(...)


class GoodsExplosiveGoodsListResp(BaseModel):
    id: Optional[Union[int, float]] = Field(None)
    goodsId: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    dtitle: Optional[str] = Field(None)
    originalPrice: Optional[float] = Field(None)
    actualPrice: Optional[float] = Field(None)
    shopType: Optional[Union[int, float]] = Field(None)
    goldSellers: Optional[Union[int, float]] = Field(None)
    monthSales: Optional[Union[int, float]] = Field(None)
    twoHoursSales: Optional[Union[int, float]] = Field(None)
    dailySales: Optional[Union[int, float]] = Field(None)
    commissionType: Optional[Union[int, float]] = Field(None)
    desc: Optional[str] = Field(None)
    couponReceiveNum: Optional[Union[int, float]] = Field(None)
    couponLink: Optional[str] = Field(None)
    couponEndTime: Optional[str] = Field(None)
    couponStartTime: Optional[str] = Field(None)
    couponPrice: Optional[float] = Field(None)
    couponConditions: Optional[str] = Field(None)
    activityType: Optional[Union[int, float]] = Field(None)
    createTime: Optional[str] = Field(None)
    mainPic: Optional[str] = Field(None)
    marketingMainPic: Optional[str] = Field(None)
    sellerId: Optional[str] = Field(None)
    cid: Optional[Union[int, float]] = Field(None)
    discounts: Optional[float] = Field(None)
    commissionRate: Optional[float] = Field(None)
    couponTotalNum: Optional[Union[int, float]] = Field(None)
    activityStartTime: Optional[str] = Field(None)
    activityEndTime: Optional[str] = Field(None)
    shopName: Optional[str] = Field(None)
    shopLevel: Optional[Union[int, float]] = Field(None)
    descScore: Optional[float] = Field(None)
    brand: Optional[Union[int, float]] = Field(None)
    brandId: Optional[Union[int, float]] = Field(None)
    brandName: Optional[str] = Field(None)
    hotPush: Optional[Union[int, float]] = Field(None)
    teamName: Optional[str] = Field(None)
    itemLink: Optional[str] = Field(None)
    tchaoshi: Optional[Union[int, float]] = Field(None)
    dsrScore: Optional[float] = Field(None)
    dsrPercent: Optional[float] = Field(None)
    shipScore: Optional[float] = Field(None)
    shipPercent: Optional[float] = Field(None)
    serviceScore: Optional[float] = Field(None)
    servicePercent: Optional[float] = Field(None)
    subcid: Optional[list] = Field(None)
    video: Optional[str] = Field(None)
    quanMLink: Optional[Union[int, float]] = Field(None)
    hzQuanOver: Optional[Union[int, float]] = Field(None)
    yunfeixian: Optional[Union[int, float]] = Field(None)
    estimateAmount: Optional[Union[int, float]] = Field(None)
    freeshipRemoteDistrict: Optional[Union[int, float]] = Field(None)
    specialText: Optional[List[str]] = Field(None)
    tbcid: Optional[Union[int, float]] = Field(None)


class DelanysBrandGetGoodsListResp(BaseModel):
    id: Optional[Union[int, float]] = Field(None)
    goodsId: Optional[str] = Field(None)
    cid: Optional[Union[int, float]] = Field(None)
    brandId: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    desc: Optional[str] = Field(None)
    specialText: Optional[list] = Field(None)
    commissionType: Optional[Union[int, float]] = Field(None)
    commissionRate: Optional[float] = Field(None)
    activityType: Optional[Union[int, float]] = Field(None)
    dailySales: Optional[Union[int, float]] = Field(None)
    monthSales: Optional[Union[int, float]] = Field(None)
    mainPic: Optional[str] = Field(None)
    marketingMainPic: Optional[str] = Field(None)
    video: Optional[str] = Field(None)
    originPrice: Optional[float] = Field(None)
    actualPrice: Optional[float] = Field(None)
    couponId: Optional[str] = Field(None)
    couponPrice: Optional[float] = Field(None)
    couponLink: Optional[str] = Field(None)
    couponConditions: Optional[str] = Field(None)
    couponReceiveNum: Optional[Union[int, float]] = Field(None)
    couponTotalNum: Optional[Union[int, float]] = Field(None)
    couponEndTime: Optional[str] = Field(None)
    couponStartTime: Optional[str] = Field(None)
    discount: Optional[float] = Field(None)
    freeshipRemoteDistrct: Optional[Union[int, float]] = Field(None)
    dTitle: Optional[str] = Field(None)


CategoryGetTbTopicListResp = Any
GoodsActivityGoodsListResp = Any
GoodsFirstOrderGiftMoneyResp = Any
GoodsFriendsCircleListResp = Any
GoodsGetCollectionListResp = Any
GoodsGetNewestGoodsResp = Any
GoodsGetOwnerGoodsResp = Any
GoodsGetStaleGoodsByTimeResp = Any
GoodsLivematerialGoodsListResp = Any
GoodsPullGoodsByTimeResp = Any
GoodsTopicCatalogue = Any
GoodsTopicGoodsListResp = Any
TbServiceActivityLinkResp = Any
TbServiceGetOrderDetailsResp = Any
TbServiceParseContentResp = Any
TbServiceTwdToTwdResp = Any
